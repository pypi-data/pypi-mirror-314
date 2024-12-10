class SqlQueries:
    @staticmethod
    def find_unused_redundant_indexes():
        """Returns a query to find unused and redundant indexes."""
        return """
        WITH unused_indexes AS (
            SELECT
                i.relname AS index_name,
                t.relname AS table_name,
                pg_size_pretty(pg_relation_size(i.oid)) AS index_size,
                s.idx_scan AS index_scans
            FROM
                pg_stat_user_indexes AS s
            JOIN
                pg_index AS idx ON s.indexrelid = idx.indexrelid
            JOIN
                pg_class AS i ON i.oid = s.indexrelid
            JOIN
                pg_class AS t ON t.oid = idx.indrelid
            WHERE
                s.idx_scan = 0
                AND NOT idx.indisprimary
                AND NOT idx.indisunique
        ),
        redundant_indexes AS (
             SELECT
            tnsp.nspname AS schema_name,
            trel.relname AS table_name,
            irel.relname AS index_name,
            string_agg(a.attname, ', ' ORDER BY c.ordinality) AS columns
          FROM pg_index AS i
          JOIN pg_class AS trel ON trel.oid = i.indrelid
          JOIN pg_namespace AS tnsp ON trel.relnamespace = tnsp.oid
          JOIN pg_class AS irel ON irel.oid = i.indexrelid
          JOIN pg_attribute AS a ON trel.oid = a.attrelid
          JOIN LATERAL unnest(i.indkey) 
            WITH ORDINALITY AS c(colnum, ordinality)
              ON a.attnum = c.colnum
          GROUP BY i, tnsp.nspname, trel.relname, irel.relname
        ),
        redundant_list AS(
        SELECT
          i.schema_name AS "schema_name",
          i.table_name,
          i.index_name AS "index_name",
          i.columns AS "columns_list",
          j.index_name AS "existsing_index",
          j.columns AS "existing_columns"
        FROM redundant_indexes i
        JOIN redundant_indexes j
          ON i.schema_name = j.schema_name
          AND i.table_name = j.table_name
          AND j.columns LIKE i.columns || ',%'
        )
        SELECT
            r.schema_name AS schema_name,
            u.table_name AS table_name,
            u.index_name AS index_name,
            u.index_scans AS index_scans,
            u.index_size AS index_size
        FROM
            unused_indexes u
        JOIN
            redundant_list r ON u.index_name = r.index_name;
        """

    @staticmethod
    def find_unused_indexes():
        """Returns indexes that never scanned and are not pk or constraint."""
        return """
            SELECT
                s.schemaname AS schema_name,
                t.relname AS table_name,
                i.relname AS index_name,
                idx_scan AS index_scans,
                pg_size_pretty(pg_relation_size(i.oid)) AS index_size
            FROM
                pg_stat_user_indexes AS s
            JOIN
                pg_index AS idx ON s.indexrelid = idx.indexrelid
            JOIN
                pg_class AS i ON i.oid = s.indexrelid
            JOIN
                pg_class AS t ON t.oid = idx.indrelid
            WHERE
                s.idx_scan=0
                AND NOT idx.indisprimary
                AND NOT idx.indisunique
            ORDER BY
                idx_scan DESC;
        """

    @staticmethod
    def find_invalid_indexes():
        """Returns a query to list all indexes which scanned over last year"""
        return """
            SELECT
                s.schemaname AS schema_name,
                t.relname AS table_name,
                i.relname AS index_name,
                idx_scan AS index_scans,
                pg_size_pretty(pg_relation_size(i.oid)) AS index_size
            FROM
                pg_stat_user_indexes AS s
            JOIN
                pg_index AS idx ON s.indexrelid = idx.indexrelid
            JOIN
                pg_class AS i ON i.oid = s.indexrelid
            JOIN
                pg_class AS t ON t.oid = idx.indrelid WHERE idx.indisvalid is FALSE;
    """

    @staticmethod
    def calculate_btree_bloat():
        return """
    SELECT current_database(), 
       nspname AS schemaname, 
       tblname, 
       idxname, 
       bs * (relpages)::bigint AS real_size,
       bs * (relpages - est_pages)::bigint AS extra_size,
       100 * (relpages - est_pages)::float / relpages AS extra_pct,
       fillfactor,
       CASE WHEN relpages > est_pages_ff 
            THEN bs * (relpages - est_pages_ff) 
            ELSE 0 
       END AS bloat_size,
       100 * (relpages - est_pages_ff)::float / relpages AS bloat_pct,
       is_na
FROM (
    SELECT coalesce(1 + ceil(reltuples / floor((bs - pageopqdata - pagehdr) / (4 + nulldatahdrwidth)::float)), 0) AS est_pages,
           coalesce(1 + ceil(reltuples / floor((bs - pageopqdata - pagehdr) * fillfactor / (100 * (4 + nulldatahdrwidth)::float))), 0) AS est_pages_ff,
           bs, 
           nspname, 
           tblname, 
           idxname, 
           relpages, 
           fillfactor, 
           is_na
    FROM (
        SELECT maxalign, 
               bs, 
               nspname, 
               tblname, 
               idxname, 
               reltuples, 
               relpages, 
               idxoid, 
               fillfactor,
               (index_tuple_hdr_bm + maxalign - CASE WHEN index_tuple_hdr_bm % maxalign = 0 THEN maxalign ELSE index_tuple_hdr_bm % maxalign END + nulldatawidth + maxalign - CASE WHEN nulldatawidth = 0 THEN 0 WHEN nulldatawidth::integer % maxalign = 0 THEN maxalign ELSE nulldatawidth::integer % maxalign END) AS nulldatahdrwidth, 
               pagehdr, 
               pageopqdata, 
               is_na
        FROM (
            SELECT n.nspname, 
                   i.tblname, 
                   i.idxname, 
                   i.reltuples, 
                   i.relpages, 
                   i.idxoid, 
                   i.fillfactor,
                   current_setting('block_size')::numeric AS bs,
                   CASE WHEN version() ~ 'mingw32' OR version() ~ '64-bit|x86_64|ppc64|ia64|amd64' THEN 8 ELSE 4 END AS maxalign,
                   24 AS pagehdr,
                   16 AS pageopqdata,
                   CASE WHEN max(coalesce(s.null_frac, 0)) = 0 THEN 8 ELSE 8 + ((32 + 8 - 1) / 8) END AS index_tuple_hdr_bm,
                   sum((1 - coalesce(s.null_frac, 0)) * coalesce(s.avg_width, 1024)) AS nulldatawidth,
                   max(CASE WHEN i.atttypid = 'pg_catalog.name'::regtype THEN 1 ELSE 0 END) > 0 AS is_na
            FROM (
                SELECT ct.relname AS tblname, 
                       ct.relnamespace, 
                       ic.idxname, 
                       ic.attpos, 
                       ic.indkey, 
                       ic.indkey[ic.attpos], 
                       ic.reltuples, 
                       ic.relpages, 
                       ic.tbloid, 
                       ic.idxoid, 
                       ic.fillfactor,
                       coalesce(a1.attnum, a2.attnum) AS attnum, 
                       coalesce(a1.attname, a2.attname) AS attname, 
                       coalesce(a1.atttypid, a2.atttypid) AS atttypid,
                       CASE WHEN a1.attnum IS NULL THEN ic.idxname ELSE ct.relname END AS attrelname
                FROM (
                    SELECT idxname, 
                           reltuples, 
                           relpages, 
                           tbloid, 
                           idxoid, 
                           fillfactor, 
                           indkey, 
                           pg_catalog.generate_series(1, indnatts) AS attpos
                    FROM (
                        SELECT ci.relname AS idxname, 
                               ci.reltuples, 
                               ci.relpages, 
                               i.indrelid AS tbloid, 
                               i.indexrelid AS idxoid,
                               coalesce(substring(array_to_string(ci.reloptions, ' ') from 'fillfactor=([0-9]+)')::smallint, 90) AS fillfactor,
                               i.indnatts, 
                               pg_catalog.string_to_array(pg_catalog.textin(pg_catalog.int2vectorout(i.indkey)), ' ')::int[] AS indkey
                        FROM pg_catalog.pg_index i
                        JOIN pg_catalog.pg_class ci ON ci.oid = i.indexrelid
                        WHERE ci.relam = (SELECT oid FROM pg_am WHERE amname = 'btree') 
                          AND ci.relpages > 0
                    ) AS idx_data
                ) AS ic
                JOIN pg_catalog.pg_class ct ON ct.oid = ic.tbloid
                LEFT JOIN pg_catalog.pg_attribute a1 ON ic.indkey[ic.attpos] <> 0 AND a1.attrelid = ic.tbloid AND a1.attnum = ic.indkey[ic.attpos]
                LEFT JOIN pg_catalog.pg_attribute a2 ON ic.indkey[ic.attpos] = 0 AND a2.attrelid = ic.idxoid AND a2.attnum = ic.attpos
            ) i
            JOIN pg_catalog.pg_namespace n ON n.oid = i.relnamespace
            JOIN pg_catalog.pg_stats s ON s.schemaname = n.nspname AND s.tablename = i.attrelname AND s.attname = i.attname
            WHERE n.nspname NOT IN ('pg_catalog', 'information_schema')
            GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
        ) AS rows_data_stats
    ) AS rows_hdr_pdg_stats
) AS relation_stats
ORDER BY nspname, tblname, idxname;
    """


    @staticmethod
    def find_duplicate_constraints():
        """Returns a list of unique indexes which are valid,ready and unique"""
        return """
            SELECT
                ix.schemaname,
                ix.tablename,
                ix.indexname,
                ix.indexdef,
                pg_size_pretty(pg_relation_size(cs.oid)) AS index_size
            FROM
                pg_stat_user_indexes co
                INNER JOIN pg_indexes ix ON co.indexrelname = ix.indexname
                INNER JOIN pg_index i ON co.indexrelid = i.indexrelid
                INNER JOIN pg_class AS cs ON cs.oid = co.indexrelid
            WHERE
                i.indisunique = true
                AND i.indisvalid = true
                AND i.indisready = true
            ORDER BY
                ix.tablename;
    """
    
    @staticmethod
    def find_duplicate_btrees():
        """Returns a list of unique indexes which are valid,ready and unique"""
        return """
            SELECT
                ix.schemaname,
                ix.tablename,
                ix.indexname,
                ix.indexdef,
                pg_size_pretty(pg_relation_size(cs.oid)) AS index_size
            FROM
                pg_stat_user_indexes co
                INNER JOIN pg_indexes ix ON co.indexrelname = ix.indexname
                INNER JOIN pg_index i ON co.indexrelid = i.indexrelid
                INNER JOIN pg_class AS cs ON cs.oid = co.indexrelid
            WHERE
                i.indisunique = false
                AND i.indisvalid = true
                AND i.indisready = true
            ORDER BY
                ix.tablename;
    """

    @staticmethod
    def get_index_type_by_indexname(index_name):
        """Returns a list of unique indexes which are valid,ready and unique"""
        return f"""
            SELECT
                c.relname AS index_name,
                am.amname AS index_type
            FROM
                pg_class c
            JOIN
                pg_index i ON c.oid = i.indexrelid
            JOIN
                pg_am am ON c.relam = am.oid
            WHERE
                c.relname = '{index_name}';
    """

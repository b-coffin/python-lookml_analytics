SELECT
    {{ left_tbl_name }}.*,
    {{ right_tbl_name }}.*
FROM {{ left_tbl_name }}
LEFT OUTER JOIN {{ right_tbl_name }}
    {{ join_condition }}
UNION
SELECT
    {{ left_tbl_name }}.*,
    {{ right_tbl_name }}.*
FROM {{ right_tbl_name }}
LEFT OUTER JOIN {{ left_tbl_name }}
    {{ join_condition }}
;
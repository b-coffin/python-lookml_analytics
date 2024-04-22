view: db {
    label: "ダッシュボード"
    sql_table_name: dataset.dashboard ;;

    dimension: db_id {
        label: "ダッシュボードID"
        hidden: no
        type: string
        sql: ${TABLE}.id ;;
    }

    dimension: name {
        label: "ダッシュボード名"
        type: string
        sql: ${TABLE}.name ;;
    }

}

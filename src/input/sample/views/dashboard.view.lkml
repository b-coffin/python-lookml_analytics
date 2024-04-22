view: dashboard {
    label: "ダッシュボード"
    sql_table_name: `@{project_id}`.dataset.`@{table_dashboard}` ;;

    dimension: id {
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

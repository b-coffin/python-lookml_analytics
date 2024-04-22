view: history {
    sql_table_name:
        `@{project_id}`.dataset.`@{table_history}`
    ;;

    dimension: id {
        type: string
        sql: ${TABLE}.id ;;
    }

    dimension: user_id {
        type: string
        sql: ${TABLE}.user_id ;;
    }

    dimension: dashboard_id {
        type: string
        sql: ${TABLE}.dashboard_id ;;
    }

    dimension: timestamp {
        type: date_time
        sql: ${TABLE}.timestamp ;;
    }

    dimension: run_time {
        hidden: yes
        type: number
        sql: ${TABLE}.run_time ;;
    }

    measure: run_time_sum {
        label: "実行時間の合計"
        type: sum
        sql: ${run_time} ;;
    }

    measure: run_time_sum {
        label: "実行回数"
        type: count
        sql: ${id} ;;
    }

}

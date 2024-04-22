view: user {
    label: "ユーザ"
    sql_table_name: dataset.user ;;

    dimension: id {
        label: "ユーザID"
        hidden: no
        type: string
        sql: ${TABLE}.id ;;
    }

    dimension: name {
        label: "ユーザ名"
        type: string
        sql: ${TABLE}.name ;;
    }

}

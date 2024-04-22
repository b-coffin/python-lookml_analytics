view: role {
    sql_table_name: dataset.role ;;

    dimension: id {
        type: string
        sql: ${TABLE}.id ;;
    }

    dimension: name {
        type: string
        sql: ${TABLE}.name ;;
    }

}

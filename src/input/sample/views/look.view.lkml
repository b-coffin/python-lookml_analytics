view: look {
    derived_table: {
        sql:
            SELECT DISTINCT *
            FROM `@{project_id}`.dataset.`@{table_look}`
        ;;
    }

    dimension: id {
        label: "Look ID"
        hidden: no
        type: string
        sql: ${TABLE}.id ;;
    }

    dimension: title {
        label: "Look タイトル"
        type: string
        sql: ${TABLE}.name ;;
    }

}

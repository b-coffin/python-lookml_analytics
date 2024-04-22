view: user {
    label: "ユーザー"
    sql_table_name: dataset.user ;;

    dimension: id {
        label: "ユーザーID"
        hidden: no
        type: string
        sql: ${TABLE}.id ;;
    }

    dimension: name {
        label: "ユーザー名"
        type: string
        sql: ${TABLE}.name ;;
    }

    dimension: email {
        label: "メールアドレス"
        type: string
        sql: ${TABLE}.email ;;
    }

}

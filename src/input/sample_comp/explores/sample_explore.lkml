include: "/views/dashboard.view.lkml"
include: "/views/history.view.lkml"
include: "/views/user.view.lkml"

explore: user {
    label: "ユーザ"
    view_name: user

    join: history {
        type: left_outer
        relationship: one_to_many
        sql_on:
            ${user.id} = ${history.user_id}
        ;;
    }

    join: group {
        type: left_outer
        relationship: many_to_one
        sql_on:
            ${user.id} = ${group.user_id}
        ;;
    }
}

explore: db {
    label: "ダッシュボード"
    view_name: db

    join: history {
        type: left_outer
        relationship: one_to_many
        sql_on:
            ${db.id} = ${history.dashboard_id}
        ;;
    }
}

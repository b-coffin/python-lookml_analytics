include: "/explores/common.lkml"
include: "/views/dashboard.view.lkml"
include: "/views/look.view.lkml"
include: "/views/user.view.lkml"

explore: user {
    label: "ユーザー"
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

    join: role {
        type: left_outer
        relationship: many_to_one
        sql_on:
            ${user.id} = ${role.user_id}
        ;;
    }
}

explore: dashboard {
    label: "ダッシュボード"
    view_name: dashboard

    join: history {
        type: left_outer
        relationship: one_to_many
        sql_on:
            ${dashboard.id} = ${history.dashboard_id}
        ;;
    }
}

explore: look {
    view_name: look

    join: history {
        type: left_outer
        relationship: one_to_many
        sql_on:
            ${look.id} = ${history.look_id}
        ;;
    }
}

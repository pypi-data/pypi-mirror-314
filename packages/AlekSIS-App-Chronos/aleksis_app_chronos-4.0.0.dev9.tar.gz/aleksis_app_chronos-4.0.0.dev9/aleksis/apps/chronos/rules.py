from rules import add_perm

from aleksis.core.util.predicates import (
    has_global_perm,
    has_object_perm,
    has_person,
)

from .util.predicates import (
    has_any_group_substitution_perm,
    has_any_timetable_object,
    has_group_substitution_perm,
    has_substitution_perm_by_group,
    has_supervisions_perm,
    has_timetable_perm,
)

# View timetable overview
view_timetable_overview_predicate = has_person & (
    has_any_timetable_object | has_global_perm("chronos.view_timetable_overview")
)
add_perm("chronos.view_timetable_overview_rule", view_timetable_overview_predicate)

# View timetable
view_timetable_predicate = has_person & has_timetable_perm
add_perm("chronos.view_timetable_rule", view_timetable_predicate)

# View supervisions for group, person or room
view_supervisions_predicate = has_person & has_supervisions_perm
add_perm("chronos.view_supervisions_rule", view_supervisions_predicate)

# View substitution management overview page
view_substitution_overview_predicate = has_person & (
    has_global_perm("chronos.manage_substitutions") | has_any_group_substitution_perm
)
add_perm("chronos.view_substitution_overview_rule", view_substitution_overview_predicate)

# Manage substitutions for a group
manage_substitutions_for_group_predicate = has_person & (
    has_global_perm("chronos.manage_substitutions") | has_group_substitution_perm
)
add_perm("chronos.manage_substitutions_for_group_rule", manage_substitutions_for_group_predicate)

# Add substitution
add_substitution_predicate = has_person & (
    has_global_perm("chronos.manage_substitutions")
    | has_substitution_perm_by_group
    | has_global_perm("chronos.add_lessonsubstitution")
)
add_perm("chronos.create_substitution_rule", add_substitution_predicate)

# Edit substition
edit_substitution_predicate = has_person & (
    has_global_perm("chronos.manage_substitutions")
    | has_substitution_perm_by_group
    | has_global_perm("chronos.change_lessonevent")
    | has_object_perm("chronos.change_lessonevent")
)
add_perm("chronos.edit_substitution_rule", edit_substitution_predicate)

# Delete substitution
delete_substitution_predicate = has_person & (
    has_global_perm("chronos.manage_substitutions")
    | has_substitution_perm_by_group
    | has_global_perm("chronos.delete_lessonevent")
    | has_object_perm("chronos.delete_lessonevent")
)
add_perm("chronos.delete_substitution_rule", delete_substitution_predicate)

# View substitutions
view_substitutions_predicate = has_person & (has_global_perm("chronos.manage_substitutions"))
add_perm("chronos.view_substitutions_rule", view_substitutions_predicate)

# View parent menu entry
view_menu_predicate = has_person & (view_timetable_overview_predicate)
add_perm("chronos.view_menu_rule", view_menu_predicate)

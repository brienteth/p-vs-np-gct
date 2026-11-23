theorem order_of_symmetric_group_s3 :
  let perms : List (Fin 3) := [0, 1, 2]
  let all_perms : List (List (Fin 3)) := perms.permutations
  List.length all_perms = 6 := by
  rfl

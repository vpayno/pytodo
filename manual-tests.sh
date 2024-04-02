#!/usr/bin/env bash

set -e

run_cmd() {
	printf "\n"
	echo Running: "$@"
	printf "\n"
	time "$@"
	printf "\n"
} # run_cmd()

run_sqlite3_cmd() {
	printf "\n"
	echo "Running: sqlite3 todos.db <- $*"
	printf "\n"
	run_cmd sqlite3 todos.db <<-EOF
		${@}
	EOF
} # run_sqlite3_cmd()

run_cmd rm -fv todos.db

run_cmd pdm run main show

run_sqlite3_cmd ".schema todos"
run_sqlite3_cmd "select * from todos"

for i in {1..10}; do
	run_cmd pdm run main add "task${i}" "cat${i}"
done

run_sqlite3_cmd "select * from todos"

run_cmd pdm run main update 1 --task task-one --category cat-one
run_cmd pdm run main update 5 --task task-five --category cat-five

run_cmd pdm run main complete 7

run_cmd pdm run main delete 1

run_cmd pdm run main complete 3

run_cmd pdm run main delete 7

run_cmd pdm run main show

run_sqlite3_cmd "select * from todos"

for i in 1{1..9}; do
	run_cmd pdm run main add "task${i}" "cat${i}"
done

run_sqlite3_cmd "select * from todos"

run_cmd pdm run main update 14 --task task-apple --category cat-apple
run_cmd pdm run main update 17 --task task-orange --category cat-orange

run_cmd pdm run main complete 15

run_cmd pdm run main delete 14

run_cmd pdm run main show

run_sqlite3_cmd "select * from todos"

printf "Manual tests completed successfully!\n"
printf "\n"

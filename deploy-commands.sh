docker build -t web .
heroku container:push web --app test-project-krasnozhon
heroku container:release web --app test-project-krasnozhon
heroku open --app test-project-krasnozhon

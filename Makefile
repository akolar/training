STATIC_ROOT=wsgi/training/static


all: js css

js: coffee
	@echo 'Minifying JS files'
	@uglifyjs -mc --screw-ie8 ${STATIC_ROOT}/js/*.js -o ${STATIC_ROOT}/dist/training.min.js
	@echo 'Done'

coffee:
	@echo 'Compiling Coffee scripts'
	@find ${STATIC_ROOT}/coffee -name '*.coffee' | xargs coffee -c -o ${STATIC_ROOT}/js
	@echo 'Done'

css:
	@echo 'Compiling SCSS files...'
	@scss ${STATIC_ROOT}/css/main.scss ${STATIC_ROOT}/dist/training.min.css -t compressed
	@echo 'Done'

watch:
	@while :; do\
		inotifywait -e create,delete,modify ${STATIC_ROOT}/coffee ${STATIC_ROOT}/css;\
		make all;\
	done

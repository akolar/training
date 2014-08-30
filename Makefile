STATIC_ROOT=wsgi/training/static


all: js css

js: coffee
	@uglifyjs -mc --screw-ie8 ${STATIC_ROOT}/js/*.js -o ${STATIC_ROOT}/dist/training.min.js

coffee:
	@find ${STATIC_ROOT}/coffee -name '*.coffee' | xargs coffee -c -o ${STATIC_ROOT}/js

css:
	@scss ${STATIC_ROOT}/css/main.scss ${STATIC_ROOT}/dist/training.min.css -t compressed

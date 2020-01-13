# Local Environment Setup

- Create your virtual environment; if you use `virtualenv`, eg: 
```
virtualenv -p python3 venv && source venv/bin/activate
```
- Install the project, including the requirements and pre-commit hooks: 
```
make
```
- Run the tests:
```
make test
```
- Run the linter:
```
make lint
```
- Run [black](https://github.com/psf/black) code formatter :
```
make black
```

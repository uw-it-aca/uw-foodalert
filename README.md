[![Build Status](https://api.travis-ci.com/uw-it-aca/uw-foodalert.svg?branch=develop)](https://travis-ci.org/uw-it-aca/uw-foodalert)
[![Coverage Status](https://coveralls.io/repos/github/uw-it-aca/uw-foodalert/badge.svg?branch=develop)](https://coveralls.io/github/uw-it-aca/uw-foodalert?branch=develop)

# Foodalert
This is a notification app for leftover food availability.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
Before you set up your local build you should have the following installed:
* NodeJS
* Docker

### Installing
First, clone this github repository:

`git clone https://github.com/uw-it-aca/uw-foodalert.git`

Then navigate into the repository's root directory and install node dependencies:

`cd uw-foodalert`

`npm install .`

Run Webpack to compile the project's frontend code:

`npx webpack`

Use docker-compose to build the app container:

`docker-compose build app`

#### Installing Fixtures

For the app to function correctly, the Allergen and SafeFood models must be populated with all relevant allergens and safe-to-share-foods respectively. Fixtures have been provided to load these models with example values. To load them, run the foolowing two commands:

`docker-compose run --rm app python manage.py loaddata Allergen --settings=sampleproj.settings.base`
`docker-compose run --rm app python manage.py loaddata SafeFood --settings=sampleproj.settings.base`

See Django documentation for instruction on populating these models with custom values and geneerating your own fixtures.

### Running the tests
This app has two test suites. One for the python backend and one for the JS frontend.

To run the python tests: `docker-compose run --rm app python manage.py test foodalert --settings=sampleproj.settings.base`.

To run the Javascript tests: `npx jest`.

Both commands must be run from repository root

### Running the app
To run the app simply execute `docker-compose up` from the repository's root directory.

## Contributing

### Git Workflow
To contribute to the project, create a branch off of develop to make your changes. Please follow the following naming conventions for your branch:

* For bug fixes, name your branch `bug/bug-being-fixed`
* For feature development, name your branch `feature/name-of-feature`
* For miscellaneous tasks, name your branch `task/task-being-completed`

For all of your commits, please write out a description of the changes made and the rationale behind their implementation in the commit details.

Once you have finished work on a branch, push it to gihub and submit a pull request for review by one of the project's maintainers. For the branch to be merged, both sets of unit tests should pass along with a pycodestyle check. To improves likelihood of your pull request being acceptd, run these locally before pushing (it may be worth setting up a git hook). 

### Webpack

During development, you may find it convenient to have webpack watching your files in the background and compiling them as they change. To do this, run: 

`npx webpack --watch`

### Documentation

To generate documentation for the backend app, run the following command in the repository root:

`docker-compose run --rm app sh ./docs/docs.sh`

## Authors

* [**Academic Experience Design & Delivery**](https://github.com/uw-it-aca)

See also the list of [contributors](https://github.com/uw-it-aca/uw-foodalert/contributors) who participated in this project.

## License

Copyright 2012-2016 UW Information Technology, University of Washington

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

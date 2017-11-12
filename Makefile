# Copyright 2017 The Lambda-blocks developers. See AUTHORS for details.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Makefile

# install and develop probably require admin privileges, unless they
# are run in a virtual environment.

install:
	python3 setup.py install

develop:
	pip3 install -e .

test:
	nose2-3 -s tests --with-cov

test-coverage-missing:
	nose2-3 -s tests --with-cov --coverage-report html

profile:
	python3 -m cProfile -s cumtime bin/blocks.py -f examples/unix.yml

clean:
	git clean -d -f -X

zip: clean
	cd .. && zip -FS --exclude lambdablocks/.git/\* -r lambdablocks.zip lambdablocks/

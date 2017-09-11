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

import json
import urllib

from typing import List, Any

from requests_oauthlib import OAuth1Session

from lb.registry import block
from lb.types import ReturnType
from lb.utils import ReturnEntry

@block(engine='twitter')
def twitter_search(query: str='',
                   count: int=100,
                   result_type: str='recent',
                   client_key: str='', client_secret: str='',
                   resource_owner_key: str='', resource_owner_secret: str=''):
    """
    Performs the given query on the Twitter feed, with the
    right credentials over OAuth1.  Refer to
    https://dev.twitter.com/rest/public/search
    for query options.
    """
    def inner() -> ReturnType[List[List[dict]]]:
        twitter = OAuth1Session(client_key,
                                client_secret=client_secret,
                                resource_owner_key=resource_owner_key,
                                resource_owner_secret=resource_owner_secret)
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        result = twitter.get(url, params={'q': query,
                                          'result_type': result_type,
                                          'count': count})
        return ReturnEntry(result=json.loads(result.text)['statuses'])
    return inner

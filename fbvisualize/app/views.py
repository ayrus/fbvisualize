import simplejson as json
from fbvisualize import settings
import urllib, urlparse
from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from django.template import RequestContext
import oauth2 as oauth

# Create your views here.
def index(request):
	if request.method == "POST":
		return HttpResponseRedirect(settings.FB_REQUEST_TOKEN_URL + 
			'?client_id=%s&redirect_uri=%s&scope=%s'
            % (settings.FB_APPID, urllib.quote_plus(settings.FB_CALLBACK), 
            	settings.FB_PERMISSIONS))
	else:
		return render_to_response("index.html", locals(), 
			context_instance=RequestContext(request))

def _retrieve_content(endpoint, client):
	'''
	Retrieve content from an oAuth endpoint through a client object and return
	the JSON parsed content.

	Keyword arguments:
	endpoint -- An oAuth endpoint to access.
	client -- python-oauth client object.

	Return:
	content -- JSON parsed output from the endpoint.
	endpoint -- Facebook specific paging 'next' URL (if exists).
	'''

	response, content = client.request(endpoint) 

	content = json.loads(content)

	# See if there's more data.
	try:
		endpoint = content['paging']['next']
	except KeyError:
		endpoint = None

	return content, endpoint

def _get_mutual(client, friend_id, access_token):


	endpoint = settings.FB_RETRIEVE_ID_URL + '/mutualfriends/%s?access_token=%s' % (friend_id, access_token)

	print endpoint
	
	flag = True

	mutualfriends = []

	

	content, endpoint = _retrieve_content(endpoint, client)

	mutualfriends = { friend['id'] : friend['name'] for friend in content['data'] }

	return mutualfriends


def process(request):
	consumer = oauth.Consumer(key=settings.FB_APPID, \
		secret=settings.FB_APPSECRET)

	client = oauth.Client(consumer)

	endpoint = settings.FB_RETRIEVE_ID_URL + '/friends?access_token=%s' % request.session['fb_access_token']

	flag = True

	friends_list = []

	while flag:
		#print endpoint
		content, endpoint = _retrieve_content(endpoint, client)
		if not endpoint:
			flag = False
		else:
			friends_list.extend(content['data'])

	#print len(friends)

	friends = { friend['id'] : friend['name'] for friend in friends_list }

	mutualfriends =  {}
	
	for friend_id in friends:

		mutualfriends[friend_id] = _get_mutual(client, friend_id, request.session['fb_access_token'])


	print mutualfriends



def callback(request):
	consumer = oauth.Consumer(key=settings.FB_APPID, \
		secret=settings.FB_APPSECRET)

	client = oauth.Client(consumer)

	request_url = settings.FB_ACCESS_TOKEN_URL + '?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s' % (settings.FB_APPID, settings.FB_CALLBACK, settings.FB_APPSECRET, request.GET.get('code'))

	response, content = client.request(request_url, 'GET')

	access_token = dict(urlparse.parse_qsl(content))['access_token']
	request.session['fb_access_token'] = access_token

	return redirect('process')
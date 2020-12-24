import requests


class VsomTester:

    def __init__(self, vsom_ip, user, password, verify=False):
        assert user is not None and password is not None

        self.base_url = 'https://%s/ismserver/json' % vsom_ip
        self.user = user
        self.password = password

        self.camera_ref = None
        self.stream_url = None

        self.session = requests.Session()
        self.session.verify = verify
        self._login()

    def _post(self, url, data=None):

        if data is not None:
            response = self.session.post('%s/%s' % (self.base_url, url), json=data)
        else:
            response = self.session.post('%s/%s' % (self.base_url, url))

        if not response.ok:
            reason = 'Command: %s, Data: %s' % (url, data)
            self._fail(reason)
        else:
            response = response.json()
            success = response["status"]["errorType"]

            if success != "SUCCESS":
                self._fail('Return errorType is not SUCCESS')

            return response

    def _fail(self, reason):

        print('[ERROR] %s' % reason)
        self._logout()

    def _logout(self):

        url = 'authentication/logout'
        self._post(url)
        print('[INFO] Logout to the VSOM')
        exit(1)

    def _login(self):

        url = 'authentication/login'
        json = {"username": self.user, "password": self.password, "domain": ""}
        response = self._post(url, json)

    def _get_cameras(self, camera_name):

        url = 'camera/getCameras'
        json = {"filter": {"byNameContains": camera_name,"byObjectType": "device_vs_camera", "pageInfo": {"start": 0, "limit": 100}}}
        # print(json)
        response = self._post(url, json)

        try:
            camera_ref_uid = response["data"]["items"][0]["videoController"]["deviceRef"]["refUid"]
            camera_ref_name = response["data"]["items"][0]["videoController"]["deviceRef"]["refName"]
            camera_ref_object_type = response["data"]["items"][0]["videoController"]["deviceRef"]["refObjectType"]
            camera_ref_vsom_uid = response["data"]["items"][0]["videoController"]["deviceRef"]["refVsomUid"]

        except KeyError:
            self._fail('No %s in VSOM VMS' % camera_name)

        self.camera_ref = {"refUid": camera_ref_uid, "refName": camera_ref_name, "refObjectType": camera_ref_object_type, "refVsomUid": camera_ref_vsom_uid}
        return self.camera_ref

    def get_streaming(self, camera_name, playback=None):

        url = 'camera/getStreamingDetails'
        camera_ref = self._get_cameras(camera_name)

        if playback is None:
            json = {"cameraStreamingDetailsRequest": {"cameraRefs": [camera_ref], "tokenExpiryInSecs": 3000,
                                                      "requestedStreams": "videostream1", "recordingStartTimeInSecs": 0,
                                                      "tokenType": "h2", "loadStreamProfile": True}}
        else:
            json = {"cameraStreamingDetailsRequest": {"cameraRefs": [camera_ref], "tokenExpiryInSecs": 3000,
                                                      "requestedStreams": "videostream1", "recordingStartTimeInSecs": playback,
                                                      "tokenType": "h2", "loadStreamProfile": True}}

        response = self._post(url, json)
        self.stream_url = response["data"]["cameraStreamingDetails"][0]["streamInfos"][0]["streamingFullURL"]

        return self.stream_url


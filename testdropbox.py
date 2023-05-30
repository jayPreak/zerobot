import dropbox
from dropbox.exceptions import AuthError


def get_dropbox_direct_link(path, ACCESS_TOKEN):
    try:
        dbx = dropbox.Dropbox(ACCESS_TOKEN)
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings(
            path)
        url = shared_link_metadata.url
        direct_link = url.replace('?dl=0', '?dl=1')
        return direct_link
    except AuthError as e:
        print('ERROR: Invalid access token; try re-generating an access token from the app console on the web.')
        return None


get_dropbox_direct_link(
    '/frames/S01/01x1.jpg', "sl.BfVNSwb0aC79kjUyqFBDRWXmqozZ4rU7pSXqi_vUqNo9bnwlRud6LLVinBTvibufzmk83MeIVJkLsNRdLzrI1OSfp5Xkl_yI4NeEEShsDCrhMwlLN6E4L9Fn2K1LVSJZJz3PPaY")

from django.shortcuts import render,redirect
from django.conf import settings
#from pytube import YouTube
import pyqrcode
import os,subprocess
from django.http import HttpResponse,FileResponse
#from youtube_transcript_api import YouTubeTranscriptApi
#from youtube_transcript_api.formatters import WebVTTFormatter
#pip install googletrans==4.0.0-rc1
#from googletrans import Translator
import re,base64
from django.contrib.staticfiles import finders
from django.conf import settings


class RangedFileReader(object):
    """
    Wraps a file like object with an iterator that runs over part (or all) of
    the file defined by start and stop. Blocks of block_size will be returned
    from the starting position, up to, but not including the stop point.
    """
    block_size = 8192

    def __init__(self, file_like, start=0, stop=float('inf'), block_size=None):
        """
        Args:
            file_like (File): A file-like object.
            start (int): Where to start reading the file.
            stop (Optional[int]:float): Where to end reading the file.
                Defaults to infinity.
            block_size (Optional[int]): The block_size to read with.
        """
        self.f = file_like
        self.size = len(self.f.read())
        self.block_size = block_size or RangedFileReader.block_size
        self.start = start
        self.stop = stop

    def __iter__(self):
        """
        Reads the data in chunks.
        """
        self.f.seek(self.start)
        position = self.start
        while position < self.stop:
            data = self.f.read(min(self.block_size, self.stop - position))
            if not data:
                break

            yield data
            position += self.block_size

    def parse_range_header(self, header, resource_size):
        """
        Parses a range header into a list of two-tuples (start, stop) where
        `start` is the starting byte of the range (inclusive) and
        `stop` is the ending byte position of the range (exclusive).

        Args:
            header (str): The HTTP_RANGE request header.
            resource_size (int): The size of the file in bytes.

        Returns:
            None if the value of the header is not syntatically valid.
        """
        if not header or '=' not in header:
            return None

        ranges = []
        units, range_ = header.split('=', 1)
        units = units.strip().lower()

        if units != 'bytes':
            return None

        for val in range_.split(','):
            val = val.strip()
            if '-' not in val:
                return None

            if val.startswith('-'):
                # suffix-byte-range-spec: this form specifies the last N bytes
                # of an entity-body.
                start = resource_size + int(val)
                if start < 0:
                    start = 0
                stop = resource_size
            else:
                # byte-range-spec: first-byte-pos "-" [last-byte-pos].
                start, stop = val.split('-', 1)
                start = int(start)
                # The +1 is here since we want the stopping point to be
                # exclusive, whereas in the HTTP spec, the last-byte-pos
                # is inclusive.
                stop = int(stop) + 1 if stop else resource_size
                if start >= stop:
                    return None

            ranges.append((start, stop))

        return ranges


class RangedFileResponse(FileResponse):
    """
    This is a modified FileResponse that returns `Content-Range` headers with
    the response, so browsers that request the file, can stream the response
    properly.
    """

    def __init__(self, request, file, *args, **kwargs):
        """
        RangedFileResponse constructor also requires a request, which
        checks whether range headers should be added to the response.

        Args:
            request(WGSIRequest): The Django request object.
            file (File): A file-like object.
        """
        self.ranged_file = RangedFileReader(file)
        super(RangedFileResponse, self).__init__(
            self.ranged_file, *args, **kwargs
        )

        if 'HTTP_RANGE' in request.META:
            self.add_range_headers(request.META['HTTP_RANGE'])

    def add_range_headers(self, range_header):
        """
        Adds several headers that are necessary for a streaming file
        response, in order for Safari to play audio files. Also
        sets the HTTP status_code to 206 (partial content).

        Args:
            range_header (str): Browser HTTP_RANGE request header.
        """
        self['Accept-Ranges'] = 'bytes'
        size = self.ranged_file.size
        try:
            ranges = self.ranged_file.parse_range_header(range_header, size)
        except ValueError:
            ranges = None
        # Only handle syntactically valid headers, that are simple (no
        # multipart byteranges).
        if ranges is not None and len(ranges) == 1:
            start, stop = ranges[0]
            if start >= size:
                # Requested range not satisfiable.
                self.status_code = 416
                return
            if stop >= size:
                stop = size
            self.ranged_file.start = start
            self.ranged_file.stop = stop
            self['Content-Range'] = 'bytes %d-%d/%d' % (start, stop - 1, size)
            self['Content-Length'] = stop - start
            self.status_code = 206


def ytdwn(request,link):
    try:        
        #os.system('sudo apt-get install -y ffmpeg') 
        os.system('sudo yt-dlp  -f 18 -o a.mp4 https://www.youtube.com/watch?v={}'.format(link))        
        tmp4=open('a.mp4' , 'rb')
        tmp5=tmp4.read()
        tmp4.close()
        response=HttpResponse(tmp5, content_type='video/mp4')
        response['Content-Length'] = os.path.getsize('a.mp4')
        response['Content-Disposition'] = 'filename=a.mp4'
        os.remove('a.mp4')
        '''
        video = YouTube('https://www.youtube.com/watch?v=%s' % link)
        stream = video.streams.get_highest_resolution()
        file = str(link)
        media_dir=os.path.join(settings.BASE_DIR,'media')
        stream.download(output_path=media_dir,filename=file)
        tmp4=open(media_dir + '/' + file , 'rb')
        tmp5=tmp4.read()
        tmp4.close()
        fn=stream.default_filename
        fn=re.sub(r"\s+", '_', fn)
        response=HttpResponse(tmp5, content_type='video/mp4')
        response['Content-Length'] = os.path.getsize(media_dir + '/' + file)
        response['Content-Disposition'] = 'filename=%s' % fn
        os.remove(media_dir + '/' + file)
        '''
        return response
    except:
        return HttpResponse ('Youtube Url Is Mistake!')
'''
def sub(request,lang,link):
    try:
        
        video = YouTube('https://www.youtube.com/watch?v=%s' % link)
        stream = video.streams.get_highest_resolution()
        media_dir=os.path.join(settings.BASE_DIR,'ytdown','media')
        stream.download(output_path=media_dir,filename='a.mp4')

        #srt=YouTubeTranscriptApi.get_transcript(link)
        transcripts = YouTubeTranscriptApi.list_transcripts(link)
        #if not transcripts :
        #    return HttpResponse('This Video dont have subtitle!')
        transcript = transcripts.find_transcript(['en'])
        if transcript.is_translatable :
            pars = transcript.translate(lang).fetch()
        #else :
        #    return HttpResponse('This Video is not translatable')
        fmt=WebVTTFormatter()
        vtt=fmt.format_transcript(pars)

        f=open(media_dir + '/sub.vtt', 'w', encoding='utf-8')
        f.write(vtt)
        f.close()

        subtitle='subtitles=%s/sub.vtt' % media_dir
        subprocess.run(['ffmpeg','-i', os.path.join(media_dir , 'a.mp4' ),'-vf',subtitle,os.path.join(media_dir,'out.mp4')])

        tmp4=open(media_dir + '/out.mp4' , 'rb')
        tmp5=tmp4.read()
        tmp4.close()
        fn=stream.default_filename
        fn=re.sub(r"\s+", '_', fn)
        response=HttpResponse(tmp5, content_type='video/mp4')
        response['Content-Length'] = os.path.getsize(media_dir + '/out.mp4')
        response['Content-Disposition'] = 'filename=%s' % fn
        os.remove(media_dir + '/a.mp4')
        os.remove(media_dir + '/sub.vtt')
        os.remove(media_dir + '/out.mp4')
        return response
    except:
        return HttpResponse ('This video dont have subtitle !')

def abcut(request,time,link):
    try:
        video = YouTube('https://www.youtube.com/watch?v=%s' % link)
        stream = video.streams.get_highest_resolution()
        media_dir=os.path.join(settings.BASE_DIR,'ytdown','media')
        stream.download(output_path=media_dir,filename='a.mp4')

        start_time=time[0:2] + ':' + time[2:4]
        end_time=time[4:6] + ':' + time[6:8]
        subprocess.run(['ffmpeg','-i', os.path.join(media_dir,'a.mp4' ),'-ss',start_time,'-to',end_time,os.path.join(media_dir , 'out.mp4')])

        tmp4=open(media_dir + '/out.mp4' , 'rb')
        tmp5=tmp4.read()
        tmp4.close()
        fn=stream.default_filename
        fn=re.sub(r"\s+", '_', fn)
        response=HttpResponse(tmp5, content_type='video/mp4')
        response['Content-Length'] = os.path.getsize(media_dir + '/out.mp4')
        response['Content-Disposition'] = 'attachment; filename=%s' % fn
        os.remove(media_dir + '/a.mp4')
        os.remove(media_dir + '/out.mp4')
        return response
    except:
        return HttpResponse ('Youtube Url Is Mistake!')
'''

def viddown(request,url,link):
    try:
        os.system('sudo rm /content/a.mp4')
        os.system('sudo yt-dlp  -f 18 -o /content/a.mp4 https://www.youtube.com/watch?v={}'.format(link))        
        os.system('sudo service nginx restart')
        return redirect(f'https://{url}/a.mp4')
    except:
        return ('Youtube Url Is Mistake!')
    
def ytv(request,url,link):
    try:
        os.system('sudo rm video.mp4')
        os.system('sudo yt-dlp  -f 18 -o video.mp4 https://www.youtube.com/watch?v={}'.format(link))
        os.system('sudo service nginx stop')
        os.system('sudo service nginx start')
        return redirect(f'https://{url}/video.mp4')
    except:
        return ('Youtube Url Is Mistake!')

def ytp(request,link):
    try:
        os.system('sudo yt-dlp  -f 18 -o /content/a.mp4 https://www.youtube.com/watch?v={}'.format(link))        
        filename = '/content/a.mp4'
        response = RangedFileResponse(request, open(filename, 'rb'), content_type='video/mp4')
        return response
    except:
        return ('Youtube Url Is Mistake!')  
        
def vid(request):
    try:
        link=request.GET['url']
        os.system('yt-dlp  -f 18 -o a.mp4 {}'.format(link))        
        tmp4=open('a.mp4' , 'rb')
        tmp5=tmp4.read()
        tmp4.close()
        response=HttpResponse(tmp5, content_type='video/mp4')
        response['Content-Length'] = os.path.getsize('a.mp4')
        response['Content-Disposition'] = 'filename=a.mp4'
        os.remove('a.mp4')
        return response
    except:
        return HttpResponse ('Youtube Url Is Mistake!!')
'''
def ytmp3(request,link):
    try:
        video = YouTube('https://www.youtube.com/watch?v=%s' % link)
        stream = video.streams.filter(only_audio=True).first()
        media_dir=os.path.join(settings.BASE_DIR,'ytdown','media')
        file = str(link)
        stream.download(output_path=media_dir,filename=file)
        subprocess.run(['ffmpeg','-i', os.path.join(media_dir, file),os.path.join(media_dir , 'm1.mp3' )])
        tmp4=open(media_dir + '/m1.mp3' , 'rb')
        tmp5=tmp4.read()
        tmp4.close()
        fn=stream.title + '.mp3'
        fn=re.sub(r"\s+", '_', fn)
        response = HttpResponse(tmp5 , content_type='audio/mp3' )
        response['Content-Length'] = os.path.getsize(media_dir + '/m1.mp3')
        response['Content-Disposition'] = 'attachment; filename=%s' % fn
        os.remove(media_dir + '/' + file)
        os.remove(media_dir + '/m1.mp3')
        return response
    except:
        return HttpResponse (video.description)
'''
def ytmp4(request,link):
    try:        
        #os.system('sudo apt-get install -y ffmpeg') 
        if os.path.isfile("/tmp/a.mp4"):
            os.remove("/tmp/a.mp4")
        os.system('sudo yt-dlp  -f 18 -o /tmp/a.mp4 https://www.youtube.com/watch?v={}'.format(link)) 
        urllink = settings.ERSCIYT_LINK if hasattr(settings, 'ERSCIYT_LINK') and settings.ERSCIYT_LINK else ""
        return redirect(urllink)
    except:
        return HttpResponse ('Youtube Url Is Mistake!')

def yt2mp4(request,link):
    try:        
        vidpath = finders.find('ytvid.mp4')        
        if os.path.isfile(vidpath):
            os.remove(vidpath)
        os.system('yt-dlp  -f 18 -o {} https://www.youtube.com/watch?v={}'.format(vidpath,link)) 
        return redirect("/static/ytvid.mp4")
    except:
        return HttpResponse ('Youtube Url Is Mistake!')

def shqr(request):
    try:
        pic=request.GET['idx']
        qr_code = pyqrcode.create(pic)#request.headers['HTTP_REFERER'])
        qr_code.svg('a.svg', scale=6)
        img=open('a.svg', "r")
        #image_data = base64.b64encode(img.read()).decode('utf-8')
        imgdata = "{}".format(img.read())
        return HttpResponse (imgdata)
    except:
        return HttpResponse ('Youtube Url Is Mistake!!!!')
        
def ngin(request):
    try:
        os.system('sudo apt install -y nginx')
        os.system('sudo sed -i "s/root \/var\/www\/html/root \/tmp/" /etc/nginx/sites-enabled/default')
        os.system('sudo sed -i "s/index index.html/index a.mp4 index.html/" /etc/nginx/sites-enabled/default')
        os.system('sudo service nginx restart')
        return HttpResponse ('<h4>All is OK!</h4>')
    except:
        return HttpResponse ('<h4>Installation failed!!!</h4>')
        
def helping(request):
    try:
        return HttpResponse ('''<!Doctype html><html><head></head><body>
        <p>Use address of youtube after watch like - for download video -  :<br>
        <b> YourSiteName/ytlink?url=<any video site link></b><br>
        or<br>
        enter Youtube ID after YourSiteName address - for play in firefox -  : <br>
        <b>YourSiteName/xazlZh1lTpM</b><br>        
        <a href="/static/ersci_viddown_tab2-1.4.xpi">Video download firefox Addon direct link</a><br>
        or<br>
        <a href="https://addons.mozilla.org/en-US/firefox/addon/ersci_viddown_tab2">video download firefox Addon mozilla site link</a>
        <br>
        <br>
        <a href="#" onclick="window.open('/yt/shqr?idx=' + window.location.href);">show QR Code for this site </a>
        <br>
        </p>
        <br>
        You can use /mp4/<Youtube Video ID> to play video with jump into your custom time of video<br>
        </body></html>
        ''')
    except:
        return HttpResponse ('Youtube Url Is Mistake!!!')

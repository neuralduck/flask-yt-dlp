from flask import Flask, redirect, url_for, request, render_template
import subprocess
app = Flask(__name__)
@app.route("/")
def home():
	return redirect('/video')

@app.route("/video", methods = ['GET'])
def video():
	return render_template("video.html", result = '')

@app.route("/audio")
def audio():
	return render_template("audio.html", result = '')

@app.route('/download_video', methods = ['POST'])
def download_video():
	data = request.form
	url = data['url']
	video_format = '.'+data['video_format']
	download_cmd = ['yt-dlp', url]
	filename = subprocess.run(f'yt-dlp --get-filename {url}'.split(' '), capture_output = True).stdout.decode("utf-8")[:-1]
	same = (filename.split('.')[-1] == data['video_format'])
	print(filename)
	print(same)
	new_name = ''.join(filename.split('.')[:-1])+video_format
	format_cmd = ['ffmpeg', '-i', filename, new_name]
	download = subprocess.run(download_cmd, capture_output=True)
	print(f'download return code: {download.returncode}')
	if not(same):
		convert = subprocess.run(format_cmd, capture_output=True)
		print(f'convert return code: {convert.returncode}')
	return render_template("video.html", result = f'{new_name} video downloaded')

@app.route('/download_audio', methods = ['POST'])
def download_audio():
	data = request.form
	url = data['url']
	audio_format = '.'+data['audio_format']
	download_cmd = ['yt-dlp', url]
	filename = subprocess.run(f'yt-dlp --get-filename {url}'.split(' '), capture_output = True).stdout.decode("utf-8")[:-1]
	same = (filename.split('.')[-1] == data['audio_format'])
	print(same)
	new_name = ''.join(filename.split('.')[:-1])+audio_format
	format_cmd = ['ffmpeg', '-i', filename, new_name]
	download = subprocess.run(download_cmd, capture_output=True)
	print(f'download return code: {download.returncode}')
	if not(same):
		convert = subprocess.run(format_cmd, capture_output=True)
		print(f'convert return code: {convert.returncode}')
	return render_template("audio.html", result = f'{new_name} audio downloaded')
if __name__ == "__main__":
	app.run(debug = True)
from pytube import YouTube
link = input("Enter YouTube Link: ")
yt = YouTube(link)
yt.streams.get_highest_resolution().download()
print("Downloaded!")
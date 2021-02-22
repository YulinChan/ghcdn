URL=$1
FILE=$2
REPO=$3
GITHUB_TOKEN="851c809e19737f73b84db5b32dcc1b6fa024f315"
DEPLOY_KEY="-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACBQ2v1zTrrYpqE10mJsd1vOB+hopmuPNTLo7Mmrvu9/wwAAAJjAl6ltwJep
bQAAAAtzc2gtZWQyNTUxOQAAACBQ2v1zTrrYpqE10mJsd1vOB+hopmuPNTLo7Mmrvu9/ww
AAAEAKVJ23ziJUD+pIQC6mSPOPBFRwYh8Ha45BTFrJ5n5ZzlDa/XNOutimoTXSYmx3W84H
6Gima481Mujsyau+73/DAAAADmdpdGh1YkBjaGFuLmltAQIDBAUGBw==
-----END OPENSSH PRIVATE KEY-----"
## Install dependent
sudo apt update
sudo apt install  aria2 ffmpeg curl git  -y

## name: Download video
aria2c --max-connection-per-server=16 --check-certificate=false $URL

## name: Slice video
ffmpeg -i $FILE -c copy -f hls -bsf:v h264_mp4toannexb -hls_list_size 0 -hls_segment_filename hls%4d.ts index.m3u8
rm -rf $FILE

## name: Setup Git
mkdir -p ~/.ssh/
echo $DEPLOY_KEY > ~/.ssh/id_rsa
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
ssh-keyscan github.com >> ~/.ssh/known_hosts
git config --global user.email "github@chan.im"
git config --global user.name "ghcdn"

## name: Create Github repo
curl \
-X POST \
-H "Authorization: token $GITHUB_TOKEN" \
-H "Content-Type: application/json" \
https://api.github.com/user/repos \
-d "{\"name\": \"$REPO\"}"

## name: Push to Github
mkdir -p gitdir/res/
mv index.m3u8 hls*.ts gitdir/res/
cd gitdir
git init
git add res/index.m3u8
git commit -m "add m3u8"
git remote add origin git@github.com:ghcdn/$REPO.git
git push -u origin master
for i in {0..9};do
  for j in {0..9};do
    files=(res/hls$i$j??.ts)
    if [ -f ${files[0]} ];then
      git add "${files[@]}"
      git commit -m "$i$j st commit"
      git push
    else
      exit 0
    fi
  done
done
import json             # JSON形式のデータを扱うための標準ライブラリ
import boto3            # AWSサービスとやり取りするためのライブラリ
from PIL import Image   #（Pillow）: 画像処理のためのライブラリ
import io               # 入出力操作を行うための標準ライブラリ

s3 = boto3.client('s3')

def lambda_handler(event,context): # event:トリガーされたイベント情報, context:実行環境
    # S3イベントからバケット名とオブジェクトキーを取得
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key'] # ファイル名

    # S3から画像を取得
    response = s3.get_object(Bucket=bucket, Key=key)
    image_content = response['Body'].read()

    # 画像をリサイズ
    image = Image.open(io.BytesIO(image_content))
    resized_image = image.resize((128.128))

    # リサイズした画像を保存
    output_bufer = io.BytesIO()
    resized_image.save(output_bufer, format='JPEG')
    output_bufer.seek(0) # バッファの読み取り位置を先頭に戻す

    # リサイズ画像を別のS3バケットにアップロード
    resided_bucket = 'resized-image-kizashi'
    s3.put_object(Bucket=resided_bucket, Key=key, Body=output_bufer, ContentType='image/jpeg') # アップロード時にオブジェクトのキー（ファイル名）とコンテンツタイプ（image/jpeg）を指定

    return {
        'stausCode': 200,
        'body': json.dumps('Image resized and uploaded successfully')
    }
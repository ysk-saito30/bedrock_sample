# bedrock_sample

## 基板モデルへのアクセス
1. AWSマネージメントコンソールからBedrockページにアクセスし、モデルアクセスを選択。リージョンによって利用可能なモデルに制限があるので注意。サンプルではバージニア北部リージョンを選択。
![bedrock_toppage](https://github.com/ysk-saito30/bedrock_sample/blob/images/bedrock_toppage.PNG)

2. モデルアクセスページで[Modify model access]を選択。
※初回リクエスト時は[Enable specific models]を選択。
![bedrock_model_access](https://github.com/ysk-saito30/bedrock_sample/blob/images/bedrock_model_access.PNG)

3. リクエストする対象のモデルのチェックボックスをチェックし、[Next]を選択。
![bedrock_checkbox](https://github.com/ysk-saito30/bedrock_sample/blob/images/bedrock_checkbox.png)

4. Termsの内容を確認したうえで、[Submit]を選択。
![bedrock_submit](https://github.com/ysk-saito30/bedrock_sample/blob/images/bedrock_submit.PNG)

## IAMユーザーの作成
1. AWSマネージメントコンソールからIAMページにアクセスし、[ユーザー]>[ユーザーの作成]を選択。

2. 任意のユーザー名を入力して[次へ]。
![create_iam](https://github.com/ysk-saito30/bedrock_sample/blob/images/create_iam.png)

3. [ポリシーを直接アタッチする]を選択し、許可ポリシーとして[AmazonBedrockFullAccess]にチェックを入れて[次へ]、その後IAMユーザー作成まで完了させる。
![attach_policy](https://github.com/ysk-saito30/bedrock_sample/blob/images/attach_policy.PNG)

4. ユーザー作成後、アクセスキーを生成。このアクセスキーとシークレットアクセスキーは後で使うので、覚えておく。
![get_access_key](https://github.com/ysk-saito30/bedrock_sample/blob/images/get_access_key.png)

## AWS CLIのインストール
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
上記ページの手順に従ってインストールする。

## 名前付きプロファイルの作成
以下コマンドでプロファイルを作成する。プロファイル名は任意。サンプルコードでは「bedrock_prof」にしています。
```
> aws configure --profile bedrock_prof
AWS Access Key ID [None]: (先ほど発行したアクセスキー）
AWS Secret Access Key [None]: (先ほど発行したシークレットアクセスキー）
Default region name [None]: us-east-1
Default output format [None]: json
```
プロファイルが有効になったことは以下のコマンドで確認できます。
```
> aws --profile bedrock_prof sts get-caller-identity
```
なお、作成したプロファイル情報は`~/.aws`に保存されています。

## python仮想環境の設定
仮想環境作成は任意です。
サンプル手順ではvenvで仮想環境を作成しています。

#### Windowsでの手順
```
# 適当な作業ディレクトリを作成
> cd (任意のパス)
> mkdir (任意のディレクトリ名)
> cd (作成したディレクトリ名)

# 仮想環境作成
> python -m venv ./venv
# 有効化
> .\venv\Scripts\Activate.ps1

# pythonバージョン確認
> python --version
Python 3.10.6

# pipバージョン確認とアップグレード
> pip list 
Package    Version
---------- -------
pip        22.2.1
setuptools 63.2.0

[notice] A new release of pip available: 22.2.1 -> 24.0
[notice] To update, run: python.exe -m pip install --upgrade pip

> python -m pip install --upgrade pip 
> pip list
Package    Version
---------- -------
pip        24.0
setuptools 63.2.0

# boto3をインストール
> pip install boto3
> pip list
Package         Version
--------------- -----------
boto3           1.34.127
botocore        1.34.127
jmespath        1.0.1
pip             24.0
python-dateutil 2.9.0.post0
s3transfer      0.10.1
setuptools      63.2.0
six             1.16.0
urllib3         2.2.1
```

## 実行
pythonプログラムを実行
```
python create_image_by_ai.py
```

## 参考URL
https://www.insurtechlab.net/use_amazon_bedrock/

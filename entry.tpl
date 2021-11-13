<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <title>人物機器管理システム</title>
  </head>
  <body>
    <p>認識したい人とデバイスの情報を入力してください</p>
    <form action="submit" method="post" enctype="multipart/form-data">
      <p>名前(ローマ字):<input type="text" name="Name" /></p>
      <p>IPアドレス: 192.168.200.
        <select name="IP">
          %for i in IP:
            <option value="{{i}}">{{i}}</option>
          %end
        </select>
      </p>
      <input type="file" name="file" />
      <input type="submit" />
    </form
    <p><a href="/">一覧表示</a></p>
  </body>
</html>

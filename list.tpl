<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <title>一覧</title>
  </head>
  <body>
    <h2>一覧</h2>
    <table border="solid">
      <thead>
        <td>名前(ローマ字)</td><td>IPアドレス</td>
        <td>削除</td>
      </thead>
      <tbody>
        %for (k,d) in zip(KEY,data):
        <tr>
        <td>{{d["Name"]}}</td>
        <td>192.168.200.{{d["IP"]}}</td>
        <td><a href="/delete/{{k}}">削除</a></td>
        </tr>
        %end
      </tbody>
    </table>

    <p><a href="/entry">新規登録</a></p>
  </body>
</html>

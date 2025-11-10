## 前提条件

- 回答は必ず日本語で行ってください。
    - ただし、ライブラリ名・API名・テスト名などの固有名詞は原文（通常は英語）のままで構いません。
- どのような質問に対しても、中立的な立場を保ち、偏見のない情報を提供してください。
- 発言内容の根拠を可能な限り提供してください。
    - もし根拠が不明な場合は、その旨を明記してください。

## 開発フロー

- コードの変更を行う際は、事前に計画を立ててユーザーに説明してください。
    - 事前説明には次を含めてください：変更理由、対象ファイル、変更内容の要約、リスク（影響範囲）。
    - ユーザーが明示的に「y」と言った場合のみ変更を実行してください。
    - ユーザーが明示的に「n」と言った場合は変更を実行しないでください。

- コード中のコメントは必ず日本語で記載してください（例外は固有名詞など）。

## リファクタリング

- 変数名、関数名、クラス名は分かりやすく説明的な名前に変更してください。
    - 省略形や略語は避けてください。

- 冗長なコードや重複している処理があれば共通化・関数化して、可読性と保守性を向上させてください。

- コメントやドキュメントが不足している場合は適切な説明を追加してください。
    - 特に処理上重要な部分や複雑なロジックについては詳細に説明してください。

- 不要なコード、未使用の変数、未使用のインポートがあれば削除してください。

## テスト方針

- 変更を加えたコードには必ずテストコードを追加してください。
    - 分岐網羅（C1）100%は原則目標とします。
    - 達成が困難な場合は、その理由を明記してください。

- テストコードには十分なコメントを追加し、各ケースの目的と期待結果を明確にしてください。

- 既存のテストがある場合は、変更内容に応じてテストを更新してください。

## 例外・注意事項

- 下記の import 文はローカルの静的解析でエラーになることがありますが、プロダクション環境で動作することを前提としているため、修正しないでください。
```python
import boto3
import pyspark
import awsglue
```
## コード
Option Explicit

' 週単位ヘッダー用のグローバル変数
Private g_FirstRangeDate As Date
Private g_LastRangeDate As Date
Private g_FirstWeekStart As Date
Private g_LastWeekEnd As Date
Private g_FirstCol As Integer
Private g_NumWeeks As Long
Private g_NumDays As Long
Private g_LastCol As Long

Sub DrawWBS()
    Dim ws As Worksheet
    Dim startDate As Date, endDate As Date
    Dim startCol As Integer, endCol As Integer
    Dim taskRow As Integer
    Dim col As Integer, row As Integer
    Dim lastRow As Integer
    
    ' 1. ワークシートを取得
    Set ws = ThisWorkbook.Sheets("Sheet1") ' シート名を適宜変更
    
    ' 2. 日単位セルを用意する範囲の初期化（期間: 2025/06/01 ? 2026/03/31）およびヘッダー表示
    InitRangeDates DateSerial(2025, 6, 1), DateSerial(2026, 3, 31)
    Call SetupHeader(ws)

    ' 3. 以前の色と罫線を消去（表示列は InitRangeDates で決定される）
    With ws.Range(ws.Cells(3, g_FirstCol), ws.Cells(ws.Rows.Count, g_LastCol))
        .Interior.ColorIndex = -4142 ' 色をクリア
        ' 罫線を全てクリア（再実行時に以前の外枠やセル罫線が残らないようにする）
        On Error Resume Next
        .Borders.LineStyle = xlNone
        On Error GoTo 0
    End With
    
    ' 4. 最後の行まで繰り返し処理
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).row
    
    For taskRow = 3 To lastRow
        startDate = ws.Cells(taskRow, 1).Value ' 開始日
        endDate = ws.Cells(taskRow, 2).Value   ' 終了日
        
        ' 開始日と終了日が空でない場合
        If IsDate(startDate) And IsDate(endDate) Then
            startCol = DateToColumn(startDate)
            endCol = DateToColumn(endDate)
            
            ' WBS行のセルに色をつける（連続領域をまとめて塗りつぶし、外枠を付ける）
            If startCol > endCol Then
                Dim tmpCol As Integer
                tmpCol = startCol
                startCol = endCol
                endCol = tmpCol
            End If

            With ws.Range(ws.Cells(taskRow, startCol), ws.Cells(taskRow, endCol))
                .Interior.Color = RGB(255, 255, 0) ' 黄色
            End With
            ' 連続範囲の外周に枠を付ける
            Call ApplyRangeOutline(ws.Range(ws.Cells(taskRow, startCol), ws.Cells(taskRow, endCol)))
        End If
    Next taskRow
End Sub

' ヘッダーの月と日付を設定
Sub SetupHeader(ws As Worksheet)
    Dim i As Long
    Dim col As Long
    Dim d As Date
    Dim monthStartCol As Long
    Dim monthEndCol As Long
    Dim curMonth As Long

    ' まず既存のヘッダー領域をクリアして結合を解除
    With ws.Range(ws.Cells(1, g_FirstCol), ws.Cells(2, g_LastCol))
        .Clear
        On Error Resume Next
        .UnMerge
        On Error GoTo 0
    End With

    ' 2行目: 週初めの日付のみ表示（週は月曜始まり）
    Dim wkDate As Date
    wkDate = g_FirstWeekStart
    Do While wkDate <= g_LastRangeDate
        If wkDate >= g_FirstRangeDate Then
            col = g_FirstCol + (wkDate - g_FirstRangeDate)
            ws.Cells(2, col).Value = Format(wkDate, "dd")
            ws.Cells(2, col).HorizontalAlignment = xlCenter
            ws.Cells(2, col).VerticalAlignment = xlCenter
        End If
        wkDate = DateAdd("d", 7, wkDate)
    Loop

    ' 1行目: 月表示（同一月の列を結合して「yyyy年m月」を表示）
    monthStartCol = g_FirstCol
    curMonth = Month(g_FirstRangeDate)
    For i = 0 To g_NumDays - 1
        d = DateAdd("d", i, g_FirstRangeDate)
        If Month(d) <> curMonth Then
            monthEndCol = g_FirstCol + i - 1
            With ws.Range(ws.Cells(1, monthStartCol), ws.Cells(1, monthEndCol))
                .Merge
                .Value = Format(DateAdd("d", (monthStartCol - g_FirstCol), g_FirstRangeDate), "yyyy年m月")
                .HorizontalAlignment = xlCenter
                .VerticalAlignment = xlCenter
            End With
            monthStartCol = g_FirstCol + i
            curMonth = Month(d)
        End If
    Next i
    ' 最後の月を処理
    monthEndCol = g_LastCol
    With ws.Range(ws.Cells(1, monthStartCol), ws.Cells(1, monthEndCol))
        .Merge
        .Value = Format(DateAdd("d", (monthStartCol - g_FirstCol), g_FirstRangeDate), "yyyy年m月")
        .HorizontalAlignment = xlCenter
        .VerticalAlignment = xlCenter
    End With
End Sub

' 日付から列番号を取得する関数
Function DateToColumn(d As Date) As Integer
    Dim dayOffset As Long
    ' InitRangeDates が呼ばれている前提（セルは日単位）
    If d <= g_FirstRangeDate Then
        DateToColumn = g_FirstCol
        Exit Function
    End If
    If d >= g_LastRangeDate Then
        DateToColumn = g_LastCol
        Exit Function
    End If

    dayOffset = d - g_FirstRangeDate
    DateToColumn = g_FirstCol + dayOffset
End Function

' 初期期間と週境界を設定するヘルパー
Sub InitRangeDates(startRange As Date, endRange As Date)
    g_FirstRangeDate = startRange
    g_LastRangeDate = endRange
    g_FirstCol = 4 ' 列Dから開始
    ' セルは日単位で用意する
    g_NumDays = (g_LastRangeDate - g_FirstRangeDate) + 1
    g_LastCol = g_FirstCol + g_NumDays - 1
    ' 週表示は月曜始まりに合わせる（g_FirstWeekStart は範囲開始日を含む直前の月曜）
    g_FirstWeekStart = g_FirstRangeDate - (Weekday(g_FirstRangeDate, vbMonday) - 1)
    ' 最終週の週末（日曜）を求める
    g_LastWeekEnd = g_LastRangeDate + (7 - Weekday(g_LastRangeDate, vbMonday))
    ' 週数（参考値）
    g_NumWeeks = ((g_LastWeekEnd - g_FirstWeekStart) / 7) + 1
End Sub

' 指定範囲の外周に枠線を付ける（範囲全体の四辺）
Sub ApplyRangeOutline(rng As Range)
    On Error Resume Next
    With rng
        With .Borders(xlEdgeLeft)
            .LineStyle = xlContinuous
            .Color = vbBlack
            .Weight = xlThin
        End With
        With .Borders(xlEdgeTop)
            .LineStyle = xlContinuous
            .Color = vbBlack
            .Weight = xlThin
        End With
        With .Borders(xlEdgeBottom)
            .LineStyle = xlContinuous
            .Color = vbBlack
            .Weight = xlThin
        End With
        With .Borders(xlEdgeRight)
            .LineStyle = xlContinuous
            .Color = vbBlack
            .Weight = xlThin
        End With
        ' 内側の罫線は消す（セル個別の罫線が残るのを防ぐ）
        With .Borders(xlInsideVertical)
            .LineStyle = xlNone
        End With
        With .Borders(xlInsideHorizontal)
            .LineStyle = xlNone
        End With
    End With
    On Error GoTo 0
End Sub

' シート上の塗りつぶしセルで、同一行の連続領域ごとに外枠を付ける
' 引数 rng を省略するとアクティブシートの UsedRange を使用
Sub OutlineFilledRegions(Optional rng As Range)
    Dim ws As Worksheet
    Dim rStart As Long, rEnd As Long, cStart As Long, cEnd As Long
    Dim rowIndex As Long, colIndex As Long
    Dim sh As Worksheet

    If rng Is Nothing Then
        Set sh = ActiveSheet
        Set rng = sh.UsedRange
    Else
        Set sh = rng.Worksheet
    End If

    rStart = rng.row
    rEnd = rng.row + rng.Rows.Count - 1
    cStart = rng.Column
    cEnd = rng.Column + rng.Columns.Count - 1

    For rowIndex = rStart To rEnd
        colIndex = cStart
        Do While colIndex <= cEnd
            ' 塗りつぶしセルの開始を探す
            If sh.Cells(rowIndex, colIndex).Interior.Pattern <> xlNone Then
                Dim startColIdx As Long
                startColIdx = colIndex
                ' 連続する塗りつぶしをスキップ
                Do While colIndex <= cEnd And sh.Cells(rowIndex, colIndex).Interior.Pattern <> xlNone
                    colIndex = colIndex + 1
                Loop
                ' 終了列は1つ前
                Dim endColIdx As Long
                endColIdx = colIndex - 1
                ' 該当範囲に外枠を付ける
                Call ApplyRangeOutline(sh.Range(sh.Cells(rowIndex, startColIdx), sh.Cells(rowIndex, endColIdx)))
            Else
                colIndex = colIndex + 1
            End If
        Loop
    Next rowIndex
End Sub




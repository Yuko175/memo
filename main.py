import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, GridUpdateMode


def page_1():
    # --------------------------------
    # 1) セッションの初期化
    # --------------------------------
    if "data" not in st.session_state:
        st.session_state.data = pd.DataFrame(
            {
                "名前": ["佐藤", "田中", ""],
                "業種": ["Technology", "Finance", "Healthcare"],
                "評価": ["Hot", "Warm", "Cold"],
            }
        )

    # 行の一意IDを管理するカウンタ
    if "next_idx" not in st.session_state:
        st.session_state.next_idx = 0

    # データに内部ID列 タスクID がなければ付与する
    if "タスクID" not in st.session_state.data.columns:
        n = len(st.session_state.data)
        start = st.session_state.next_idx
        ids = list(range(start, start + n))
        st.session_state.data = st.session_state.data.reset_index(drop=True)
        st.session_state.data.insert(0, "タスクID", ids)
        st.session_state.next_idx = start + n

    st.title("ページ1")

    # フォーム周りの枠線・ボックスシャドウを消す（フォームを目立たなくする）
    st.markdown(
        """
      <style>
      /* 全ての form 要素のボーダーと影を無効化 */
      form {
          border: none !important;
          box-shadow: none !important;
          background: transparent !important;
          padding: 0 !important;
          margin: 0 !important;
      }
      /* Streamlit のフォームラッパーに対する保険 */
      .stForm, .stForm > div {
          border: none !important;
          box-shadow: none !important;
          background: transparent !important;
          padding: 0 !important;
          margin: 0 !important;
      }
      </style>
      """,
        unsafe_allow_html=True,
    )

    # --------------------------------
    # 2) GridOptions の設定
    # --------------------------------
    gb = GridOptionsBuilder.from_dataframe(st.session_state.data)
    gb.configure_default_column(
        editable=True, sortable=True, filterable=True, resizable=True
    )

    # 行選択（複数行選択）を有効化
    gb.configure_selection("multiple", use_checkbox=True)
    grid_options = gb.build()

    # 行に空白セルがある場合は行全体を薄赤でハイライトする JS
    grid_options["getRowStyle"] = JsCode(
        """
      function(params) {
          var data = params.data;
          for (var k in data) {
              var v = data[k];
              if (v === null || v === undefined) { return {'backgroundColor':'#ffcccc'}; }
              if (typeof v === 'string' && v.trim() === '') { return {'backgroundColor':'#ffcccc'}; }
          }
          return null;
      }
  """
    )

    # --------------------------------
    # 3) AgGridの表示（フォーム）
    # --------------------------------
    with st.form(key="grid_form"):
        # 更新ボタンと保存ボタンを左右のカラムに配置して、保存ボタンを右側に寄せる
        col_left, col_right = st.columns([8, 1])
        # with col_left:
        #     submit_button = st.form_submit_button("🔄更新")
        with col_right:
            save_button = st.form_submit_button("保存")

        grid_response = AgGrid(
            st.session_state.data,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.MODEL_CHANGED,
            fit_columns_on_grid_load=True,
            allow_unsafe_jscode=True,
            theme="blue",
        )

        # ヘルパ: AgGrid の data を DataFrame に変換して タスクID を整備する
        def _df_from_grid_response(resp):
            if not resp or resp.get("data") is None:
                return None
            df_tmp = pd.DataFrame(resp["data"])
            if "タスクID" in df_tmp.columns:
                df_tmp["タスクID"] = pd.to_numeric(df_tmp["タスクID"], errors="coerce")
                if df_tmp["タスクID"].isna().any():
                    for i in df_tmp.index[df_tmp["タスクID"].isna()]:
                        df_tmp.at[i, "タスクID"] = st.session_state.next_idx
                        st.session_state.next_idx += 1
                df_tmp["タスクID"] = df_tmp["タスクID"].astype(int)
            else:
                n = len(df_tmp)
                ids = list(
                    range(st.session_state.next_idx, st.session_state.next_idx + n)
                )
                df_tmp.insert(0, "タスクID", ids)
                st.session_state.next_idx += n
            return df_tmp

        # # (A) 更新ボタン
        # if submit_button:
        #     df_tmp = _df_from_grid_response(grid_response)
        #     if df_tmp is not None:
        #         st.session_state.data = df_tmp
        #         st.success("更新しました")
        #     else:
        #         st.warning("更新するデータがありません")

        # 横並びにするためにカラムを作成
        col1, col2, col3 = st.columns(3)
        with col2:
            delete_button = st.form_submit_button(
                "選択行を削除", type="primary", use_container_width=True
            )

        # 保存ボタン
        # with col2:
        # save_button = st.form_submit_button("保存")

        # (B) 削除ボタン
        if delete_button:
            # フォーム内の最新値を読み取って処理する
            df_tmp = _df_from_grid_response(grid_response)
            if df_tmp is not None:
                st.session_state.data = df_tmp
            else:
                st.warning("更新するデータがありません")

            st.session_state.data = pd.DataFrame(grid_response["data"])
            st.success("更新しました")

            # フォーム内で選択されている行を取得して DataFrame にする（未定義エラーを回避）
            selected_rows = (
                grid_response.get("selected_rows") if grid_response else None
            )
            if selected_rows is not None and len(selected_rows) > 0:
                try:
                    selected_rows_df = pd.DataFrame(selected_rows)
                except Exception:
                    selected_rows_df = pd.DataFrame(selected_rows)
            else:
                selected_rows_df = pd.DataFrame()

            if not selected_rows_df.empty:
                # タスクID による削除を確認
                ids_to_delete = selected_rows_df["タスクID"].astype(int).tolist()

                # ids_to_delete に該当する行を削除
                st.session_state.data = st.session_state.data[
                    ~st.session_state.data["タスクID"].isin(ids_to_delete)
                ].reset_index(drop=True)

                # 削除後、再表示するために直接再描画
                st.rerun()
                # 削除後に更新(フォームの送信をしたいので)ポップアップで更新ボタンが表示する
                st.success("行を削除しました")
                st.balloons()
            else:
                st.warning("削除する行が選択されていません")

        # (C) 保存ボタン
        if save_button:
            # フォーム内の最新値を読み取って処理する
            df_tmp = _df_from_grid_response(grid_response)
            if df_tmp is not None:
                st.session_state.data = df_tmp
            else:
                st.warning("更新するデータがありません")

            st.session_state.data = pd.DataFrame(grid_response["data"])
            st.success("更新しました")

            # 自動でページ2に遷移
            st.session_state.page = "ページ 2"
            st.rerun()

    # AgGrid から返されるデータをセッションに反映
    if grid_response and grid_response.get("data") is not None:
        try:
            df_edited = pd.DataFrame(grid_response["data"])
            # タスクID がある行は数値化し、欠損があれば新しいIDを割り当てる
            if "タスクID" in df_edited.columns:
                df_edited["タスクID"] = pd.to_numeric(
                    df_edited["タスクID"], errors="coerce"
                )
                # 欠損値に新しいIDを割り当て
                if df_edited["タスクID"].isna().any():
                    for i in df_edited.index[df_edited["タスクID"].isna()]:
                        df_edited.at[i, "タスクID"] = st.session_state.next_idx
                        st.session_state.next_idx += 1
                df_edited["タスクID"] = df_edited["タスクID"].astype(int)
            else:
                # タスクID 列が無ければ新たに付与
                n = len(df_edited)
                ids = list(
                    range(st.session_state.next_idx, st.session_state.next_idx + n)
                )
                df_edited.insert(0, "タスクID", ids)
                st.session_state.next_idx += n

            st.session_state.data = df_edited
        except Exception:
            st.session_state.data = grid_response["data"]

    # 選択された行を取得
    selected_rows = grid_response.get("selected_rows") if grid_response else None
    if selected_rows is not None and len(selected_rows) > 0:
        try:
            selected_rows_df = pd.DataFrame(selected_rows)
        except Exception:
            selected_rows_df = pd.DataFrame(selected_rows)
    else:
        selected_rows_df = pd.DataFrame()

    # --------------------------------
    # 4) ボタンによる行操作
    # --------------------------------
    col1, col2, col3 = st.columns(3)
    # ボタンの場所を中央
    # ボタンのCSSスタイルを変更（色、フォント、配置）
    button_css = """
    <style>
      div.stButton > button:first-child {
        margin: 0 auto;                    /* ボタンを中央に配置 */
        display      : block;               /* ボタンをブロック要素に変更 */
        padding      : 0.4em 1.2em;         /* パディングを設定 */
        border       : none;                /* ボーダーなし */
        border-radius: 0.5em;               /* 角丸を強調 */
        color        : white;               /* 文字色を白に */
        font-size    : 1.1em;               /* 文字サイズを少し大きく */
        line-height  : 1.5em;               /* 行の高さを調整 */
        text-align   : center;              /* 文字の位置を中央揃え */
        font-weight  : bold;                /* 太字にする */
        background   : #39d353;             /* 蛍光の緑色 */
      }
      
      div.stButton > button:first-child:hover {
        background-color: #28a745;         /* ホバー時の色変更 */
      }
    </style>
    """
    st.markdown(button_css, unsafe_allow_html=True)
    if col2.button("タスクを追加", use_container_width=True):
        new_row = pd.DataFrame(
            [
                {
                    "タスクID": st.session_state.next_idx,
                    "名前": "",
                    "業種": "",
                    "評価": "",
                }
            ]
        )
        st.session_state.next_idx += 1
        st.session_state.data = pd.concat(
            [st.session_state.data, new_row], ignore_index=True
        )
        # 追加後、再表示するために直接再描画
        st.rerun()


def page_2():
    st.title("ページ 2")
    st.write("これはページ 2 です。")
    # st.writeでセッションデータを表示
    st.write("現在のデータ:")
    st.dataframe(st.session_state.data.drop(columns="タスクID", errors="ignore"))
    # 戻る
    if st.button("戻る"):
        st.session_state.page = "ページ 1"
        st.rerun()


# メインのアプリケーション
def main():
    # ページの選択をセッションステートに保存
    if "page" not in st.session_state:
        st.session_state.page = "ページ 1"

    # st.sidebar.title("ページ選択")
    # page = st.sidebar.radio("ページを選択", ("ページ 1", "ページ 2"))

    if st.session_state.page == "ページ 1":
        page_1()
    elif st.session_state.page == "ページ 2":
        page_2()


if __name__ == "__main__":
    main()

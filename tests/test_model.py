from kenallclient import model


class TestKenAllSearchResult:
    def test_fromdict(self, dummy_search_json):
        result = model.KenAllSearchResult.fromdict(dummy_search_json)
        assert result == model.KenAllSearchResult(
            version="2021-02-26",
            query="神奈川県 AND 日本郵便",
            count=3,
            offset=0,
            limit=100,
            facets=[
                ("/神奈川県", 3),
            ],
            data=[
                model.KenAllResultItem(
                    jisx0402="14131",
                    old_code="210",
                    postal_code="2108797",
                    prefecture_kana="",
                    city_kana="",
                    town_kana="",
                    town_kana_raw="",
                    prefecture="神奈川県",
                    city="川崎市川崎区",
                    town="榎町",
                    koaza="",
                    kyoto_street="",
                    building="",
                    floor="",
                    town_partial=False,
                    town_addressed_koaza=False,
                    town_chome=False,
                    town_multi=False,
                    town_raw="榎町",
                    corporation=model.KenAllCorporation(
                        name="日本郵便　株式会社　南関東支社",
                        name_kana="ニツポンユウビン　カブシキガイシヤ　ミナミカントウシシヤ",
                        block_lot="１－２",
                        block_lot_num="1-2",
                        post_office="川崎港",
                        code_type=0,
                    ),
                ),
                model.KenAllResultItem(
                    jisx0402="14131",
                    old_code="210",
                    postal_code="2108796",
                    prefecture_kana="",
                    city_kana="",
                    town_kana="",
                    town_kana_raw="",
                    prefecture="神奈川県",
                    city="川崎市川崎区",
                    town="榎町",
                    koaza="",
                    kyoto_street="",
                    building="",
                    floor="",
                    town_partial=False,
                    town_addressed_koaza=False,
                    town_chome=False,
                    town_multi=False,
                    town_raw="榎町",
                    corporation=model.KenAllCorporation(
                        name="日本郵便　株式会社　神奈川監査室",
                        name_kana="ニツポンユウビン　カブシキガイシヤ　カナガワカンサシツ",
                        block_lot="１－２",
                        block_lot_num="1-2",
                        post_office="川崎港",
                        code_type=0,
                    ),
                ),
                model.KenAllResultItem(
                    jisx0402="14131",
                    old_code="210",
                    postal_code="2108793",
                    prefecture_kana="",
                    city_kana="",
                    town_kana="",
                    town_kana_raw="",
                    prefecture="神奈川県",
                    city="川崎市川崎区",
                    town="榎町",
                    koaza="",
                    kyoto_street="",
                    building="",
                    floor="",
                    town_partial=False,
                    town_addressed_koaza=False,
                    town_chome=False,
                    town_multi=False,
                    town_raw="榎町",
                    corporation=model.KenAllCorporation(
                        name="日本郵便　株式会社　南関東支社　郵便事業本部　（三種）",
                        name_kana="ニホンユウビン　カブシキガイシヤ　ミナミカントウシシヤ　ユウビンジギヨウホンブ　（サンシユ）",
                        block_lot="１－２",
                        block_lot_num="1-2",
                        post_office="川崎港",
                        code_type=0,
                    ),
                ),
            ],
        )


class TestKenAllResult:
    def test_fromdict(self, dummy_json):
        result = model.KenAllResult.fromdict(dummy_json)
        assert result == model.KenAllResult(
            version="2020-11-30",
            data=[
                model.KenAllResultItem(
                    jisx0402="13101",
                    old_code="100",
                    postal_code="1008105",
                    prefecture_kana="",
                    city_kana="",
                    town_kana="",
                    town_kana_raw="",
                    prefecture="東京都",
                    city="千代田区",
                    town="大手町",
                    koaza="",
                    kyoto_street="",
                    building="",
                    floor="",
                    town_partial=False,
                    town_addressed_koaza=False,
                    town_chome=False,
                    town_multi=False,
                    town_raw="大手町",
                    corporation=model.KenAllCorporation(
                        name="チッソ　株式会社",
                        name_kana="ﾁﾂｿ ｶﾌﾞｼｷｶﾞｲｼﾔ",
                        block_lot="２丁目２－１（新大手町ビル）",
                        block_lot_num="2-2-1",
                        post_office="銀座",
                        code_type=0,
                    ),
                )
            ],
        )


class TestHolidaySearchResult:
    def test_fromdict(self, dummy_holiday_search_json):
        result = model.HolidaySearchResult.fromdict(dummy_holiday_search_json)
        assert result == model.HolidaySearchResult(
            data=[
                model.Holiday(
                    title="元日",
                    date="2022-01-01",
                    day_of_week=6,
                    day_of_week_text="saturday",
                ),
                model.Holiday(
                    title="成人の日",
                    date="2022-01-10",
                    day_of_week=1,
                    day_of_week_text="monday",
                ),
                model.Holiday(
                    title="建国記念の日",
                    date="2022-02-11",
                    day_of_week=5,
                    day_of_week_text="friday",
                ),
                model.Holiday(
                    title="天皇誕生日",
                    date="2022-02-23",
                    day_of_week=3,
                    day_of_week_text="wednesday",
                ),
                model.Holiday(
                    title="春分の日",
                    date="2022-03-21",
                    day_of_week=1,
                    day_of_week_text="monday",
                ),
                model.Holiday(
                    title="昭和の日",
                    date="2022-04-29",
                    day_of_week=5,
                    day_of_week_text="friday",
                ),
                model.Holiday(
                    title="憲法記念日",
                    date="2022-05-03",
                    day_of_week=2,
                    day_of_week_text="tuesday",
                ),
                model.Holiday(
                    title="みどりの日",
                    date="2022-05-04",
                    day_of_week=3,
                    day_of_week_text="wednesday",
                ),
                model.Holiday(
                    title="こどもの日",
                    date="2022-05-05",
                    day_of_week=4,
                    day_of_week_text="thursday",
                ),
                model.Holiday(
                    title="海の日",
                    date="2022-07-18",
                    day_of_week=1,
                    day_of_week_text="monday",
                ),
                model.Holiday(
                    title="山の日",
                    date="2022-08-11",
                    day_of_week=4,
                    day_of_week_text="thursday",
                ),
                model.Holiday(
                    title="敬老の日",
                    date="2022-09-19",
                    day_of_week=1,
                    day_of_week_text="monday",
                ),
                model.Holiday(
                    title="秋分の日",
                    date="2022-09-23",
                    day_of_week=5,
                    day_of_week_text="friday",
                ),
                model.Holiday(
                    title="スポーツの日",
                    date="2022-10-10",
                    day_of_week=1,
                    day_of_week_text="monday",
                ),
                model.Holiday(
                    title="文化の日",
                    date="2022-11-03",
                    day_of_week=4,
                    day_of_week_text="thursday",
                ),
                model.Holiday(
                    title="勤労感謝の日",
                    date="2022-11-23",
                    day_of_week=3,
                    day_of_week_text="wednesday",
                ),
            ]
        )

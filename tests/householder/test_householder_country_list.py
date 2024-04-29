from solar_offset.db import get_db


def test_countries(app, client, captured_templates):

    with app.app_context():
        db = get_db()

        _ = client.get("/countries?raw")

        assert len(captured_templates) == 1

        template, context = captured_templates[0]
        assert template.name == "./users/householder/country_list.html"
        assert 'countries' in context
        assert all([ 'donation_sum' in info for info in context['countries'] ])
        assert all([ 'avg_solar_hours' in info for info in context['countries'] ])
        assert all([ 'solar_panel_price' in info for info in context['countries'] ])
        assert all([ 'carbon_offset_per_pound' in info for info in context['countries'] ])
        assert all([ 'carbon_offset_per_panel_kg' in info for info in context['countries'] ])
        assert all([ 'solar_panel_percent_footprint' in info for info in context['countries'] ])
        assert all([ 'population_size' in info for info in context['countries'] ])
        assert all([ 'name' in info for info in context['countries'] ])
        assert all([ 'country_code' in info for info in context['countries'] ])
        assert all([ 'short_code' in info for info in context['countries'] ])

        count_countries = db.execute("SELECT COUNT(country_code) AS code_count \
                                     FROM country;").fetchone()["code_count"]
        assert count_countries == len(context['countries'])


def test_countries_donation_sums(app, client, captured_templates):
    with app.app_context():
        _ = client.get("/countries")

        assert len(captured_templates) == 1
        _, context = captured_templates[0]
        
        country_list = context['countries']

        db = get_db()
        donations = db.execute("SELECT * FROM donation").fetchall()
        print([ dict(d) for d in donations ])

        for country_json in country_list:
            print(f"Country: {country_json['country_code']}")
            country_donations = [ d['donation_amount'] for d in donations if str(d['country_code']) == str(country_json['country_code']) ]

            print(f"Donation Stats in Country List Page: count={country_json['donation_count']}, total={country_json['donation_sum']}")
            print(f"Manually Summed Donations:           count={len(country_donations)}, total={sum(country_donations)}")

            assert country_json['donation_count'] == len(country_donations)
            assert country_json['donation_sum'] == sum(country_donations)
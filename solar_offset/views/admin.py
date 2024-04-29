from flask import Blueprint, render_template, request, redirect, g
from solar_offset.db import get_db
from solar_offset.views.auth import login_required
from solar_offset.utils.statistics_util import admin_dashboard_statistics
from solar_offset.utils.carbon_offset_util import SOLAR_PANEL_POWER_kW

bp = Blueprint("admin", __name__)


@bp.route("/admin", methods=["GET", "POST"])
@login_required("a")
def admin():
    db = get_db()

    # User's Data preparation
    current_admin = g.user['id']
    users = db.execute(
        'SELECT * FROM user WHERE id!= ? ', (current_admin,)
    ).fetchall()

    user_dicts = [ dict(usr) for usr in users ]
    for usr in user_dicts:
        user_types = []
        if "h" in usr["user_type"]:
            user_types.append("Householder")
        if "s" in usr["user_type"]:
            user_types.append("Staff")
        if 'a' in usr['user_type']:
            user_types.append("Admin")
        usr['user_type'] = " & ".join(user_types)

        usr['is_suspended'] = usr['status_suspend'] is not None
        usr['suspend_message'] = usr['status_suspend'] if usr['is_suspended'] else '-'

    print(user_dicts)

    # Donataion Data Preparation
    donations_rows = db.execute(
        "SELECT donation.*, country.name AS country_name, country.solar_panel_price_per_kw, \
                organization.name AS organization_name, user.email_username AS householder \
            FROM donation JOIN country JOIN organization JOIN user \
            ON (donation.country_code == country.country_code) \
                AND (donation.organization_slug == organization.name_slug) \
                AND (donation.householder_id == user.id) \
            ORDER BY donation.created DESC;"
    ).fetchall()

    donations = []
    for d in donations_rows:
        donations.append(
            {
                'created': d['created'].strftime('%Y-%m-%d %H:%M'),
                'country_name': d['country_name'],
                'organization_name': d['organization_name'],
                'amount': d['donation_amount'],
                'solar_panels': round(d['donation_amount'] / (SOLAR_PANEL_POWER_kW * d['solar_panel_price_per_kw'])),
                'householder': d['householder']
            }
        )

    total_donations_chart, donation_frequency_chart, avg_donation_chart, user_type_chart = admin_dashboard_statistics(donations, user_dicts)


    return render_template(
        "./users/admin/admin.html",
        users=user_dicts,
        total_donations_chart=total_donations_chart,
        donation_frequency_chart=donation_frequency_chart,
        avg_donation_chart=avg_donation_chart,
        user_type_chart=user_type_chart
    )


@bp.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form['user_id']
    db = get_db()
    db.execute("DELETE FROM user WHERE id == ?", (user_id,))
    db.commit()
    return redirect('/admin')


@bp.route('/is-suspend-user', methods=['POST'])
def is_suspend_user():
    user_id = request.form['user_id']
    db = get_db()

    if 'suspend_message' in request.form:
        suspend_message = request.form['suspend_message']
        db.execute(
            "UPDATE user SET status_suspend = ? WHERE id == ?",
            (suspend_message, user_id),
        )
    else:
        db.execute(
            "UPDATE user SET status_suspend = ? WHERE id == ?",
            (None, user_id),
        )

    db.commit()
    return redirect('/admin')

from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': '6th_sem_internship_apdcl',
}


@app.route('/users', methods=['GET'])
def get_users():
    try:
        button = request.args.get('button')
        consumer_number = request.args.get('consumer_number')

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        if button == "get_consumer_number":
            query = "select name,mobile_number,address,user_connection_type,user.meter_number,electric_connection.connected_load from user INNER JOIN electric_connection on user.meter_number = electric_connection.meter_number where consumer_number =" + consumer_number + ";"

        elif button == 'get_prepaid_balance':
            query = "select amount_paid,due_amount from bills where bill_date = (SELECT bill_date FROM bills WHERE consumer_number =" + consumer_number + " ORDER BY bill_date DESC LIMIT 1);"

        elif button == 'get_last_bill_details':
            query = "select bill_number,bill_date,amount_paid,due_amount,due_date,transaction_mode from bills where bill_date = (SELECT bill_date FROM bills WHERE consumer_number = " + consumer_number + " ORDER BY bill_date DESC LIMIT 1);"
        
        elif button == 'get_last_recharge_details':
            query = "select bill_number,bill_date,amount_paid,due_amount,due_date,transaction_mode from bills where bill_date = (SELECT bill_date FROM bills WHERE consumer_number = " + consumer_number + " ORDER BY bill_date DESC LIMIT 1);"

        elif button == "update_mobile_number":
            mobile_number = request.args.get('mobile_number')
            update_query = "update user set mobile_number='" + mobile_number + "' where consumer_number = " + consumer_number + ";"
            cursor.execute(update_query)
            connection.commit()
            query = "select name,mobile_number from user where consumer_number = " + consumer_number + ";"

        elif button == 'get_tips':
            tip_id = request.args.get('tip_id')
            query = "select tip_details from tips where tip_number = " + tip_id + ";"

        elif button == 'lodge_complaint':
            complaint = request.args.get('complaint')
            query = "insert into complaints(consumer_number,complaint_details) values('" + consumer_number + "','" + complaint + "');"

        else:
            return jsonify({'error': 'Invalid button parameter.', 'btn': button,
                            'consumer_num': consumer_number}), 400

        cursor.execute(query)

        # Fetch all the rows
        rows = cursor.fetchall()
        if(len(rows) == 0):
            user = None
            user = {
                'msg': 'error'
            }
        # Prepare the response data as a list of dictionaries
        else:
            for row in rows:
                if button == "get_consumer_number":
                    user = None
                    user = {
                        'name': row[0],
                        'mobile_number': row[1],
                        'address': row[2],
                        'user_connection_type': row[3],
                        'meter_number': row[4],
                        'connected_load': row[5],
                        'msg': 'success'
                    }

                elif button == 'get_prepaid_balance':
                    user = None
                    user = {
                        'amount_paid': row[0],
                        'due_amount': row[1],
                        'msg': 'success'
                    }

                elif button == 'get_last_bill_details':
                    user = None
                    user = {
                        'bill_number': row[0],
                        'bill_date': row[1],
                        'amount_paid': row[2],
                        'due_amount': row[3],
                        'due_date': row[4],
                        'transaction_mode': row[5],
                        'msg': 'success'
                    }

                elif button == 'get_last_recharge_details':
                    user = None
                    user = {
                        'bill_number': row[0],
                        'bill_date': row[1],
                        'amount_paid': row[2],
                        'due_amount': row[3],
                        'due_date': row[4],
                        'transaction_mode': row[5],
                        'msg': 'success'
                    }

                elif button == 'update_mobile_number':
                    user = None
                    user = {
                        'name' : row[0],
                        'mobile_number' : row[1],
                        'msg': 'success'
                    }

                elif button == 'get_tips':
                    user = None
                    user = {
                        'tip_details': row[0],
                        'msg': 'success'
                    }

        if button == 'lodge_complaint':
            connection.commit()
            user = None
            user = {
                'msg': 'success'
            }

        cursor.close()
        connection.close()

        return jsonify(user)

    except Exception as e:
        return jsonify(
            {'error': 'An error occurred while fetching data: ' + str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

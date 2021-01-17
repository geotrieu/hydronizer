#!/usr/bin/env python3
"""
Test psycopg with CockroachDB.
"""

import time
import random
import logging
from argparse import ArgumentParser, RawTextHelpFormatter

import psycopg2
from psycopg2.errors import SerializationFailure


def create_accounts(conn):
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS water_breaks (id INT PRIMARY KEY, time INT, quantity INT)"
        )
        cur.execute("UPSERT INTO water_breaks (id, time, quantity) VALUES (1, 2, 3)")
        logging.debug("create_entry(): status message: %s", cur.statusmessage)
    conn.commit()


def delete_accounts(conn):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM bank.accounts")
        logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    conn.commit()


def print_breaks(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id, balance FROM water_breaks")
        logging.debug("print_breaks(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        print(f"Breaks at {time.asctime()}:")
        for row in rows:
            print(row)

def test_retry_loop(conn):
    """
    Cause a seralization error in the connection.

    This function can be used to test retry logic.
    """
    with conn.cursor() as cur:
        # The first statement in a transaction can be retried transparently on
        # the server, so we need to add a dummy statement so that our
        # force_retry() statement isn't the first one.
        cur.execute("SELECT now()")
        cur.execute("SELECT crdb_internal.force_retry('1s'::INTERVAL)")
    logging.debug("test_retry_loop(): status message: %s", cur.statusmessage)


def main():
    opt = parse_cmdline()
    logging.basicConfig(level=logging.DEBUG if opt.verbose else logging.INFO)

    conn = psycopg2.connect(opt.dsn)
    create_accounts(conn)
    print_balances(conn)

    amount = 100
    fromId = 1
    toId = 2

    try:
        run_transaction(conn, lambda conn: transfer_funds(conn, fromId, toId, amount))

        # The function below is used to test the transaction retry logic.  It
        # can be deleted from production code.
        # run_transaction(conn, test_retry_loop)
    except ValueError as ve:
        # Below, we print the error and continue on so this example is easy to
        # run (and run, and run...).  In real code you should handle this error
        # and any others thrown by the database interaction.
        logging.debug("run_transaction(conn, op) failed: %s", ve)
        pass

    print_balances(conn)

    delete_accounts(conn)

    # Close communication with the database.
    conn.close()


def parse_cmdline():
    parser = ArgumentParser(description=__doc__,
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "dsn",
        help="database connection string\n\n"
             "For cockroach demo, use postgresql://<username>:<password>@<hostname>:<port>/bank?sslmode=require,\n"
             "with the username and password created in the demo cluster, and the hostname and port listed in the\n"
             "(sql/tcp) connection parameters of the demo cluster welcome message."
    )

    parser.add_argument("-v", "--verbose",
                        action="store_true", help="print debug info")

    opt = parser.parse_args()
    return opt


if __name__ == "__main__":
    main()
    
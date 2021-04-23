/*
   BAREOS® - Backup Archiving REcovery Open Sourced

   Copyright (C) 2009-2011 Free Software Foundation Europe e.V.
   Copyright (C) 2016-2016 Planets Communications B.V.
   Copyright (C) 2016-2021 Bareos GmbH & Co. KG

   This program is Free Software; you can redistribute it and/or
   modify it under the terms of version three of the GNU Affero General Public
   License as published by the Free Software Foundation and included
   in the file LICENSE.

   This program is distributed in the hope that it will be useful, but
   WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
   Affero General Public License for more details.

   You should have received a copy of the GNU Affero General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
   02110-1301, USA.
*/
#ifndef BAREOS_CATS_BDB_SQLITE_H_
#define BAREOS_CATS_BDB_SQLITE_H_

#include "include/bareos.h"
#include "cats/column_data.h"

#include <string>
#include <vector>

struct AttributesDbRecord;
class JobControlRecord;

class BareosDbSqlite : public BareosDbPrivateInterface {
 private:
  struct sqlite3* db_handle_;
  char** result_; /**< sql_store_results() and SqlQueryWithoutHandler() */
  char**
      col_names_; /**< used to access fields when using SqlQueryWithHandler() */
  char* lowlevel_errmsg_;
  SQL_FIELD sql_field_; /**< used when using SqlQueryWithHandler() and
                           SqlFetchField() */
  static const char*
      query_definitions[]; /**< table of predefined sql queries */

 private:
  bool OpenDatabase(JobControlRecord* jcr) override;
  void CloseDatabase(JobControlRecord* jcr) override;
  bool ValidateConnection(void) override;
  void ThreadCleanup(void) override;
  void StartTransaction(JobControlRecord* jcr) override;
  void EndTransaction(JobControlRecord* jcr) override;
  bool SqlQueryWithHandler(const char* query,
                           DB_RESULT_HANDLER* ResultHandler,
                           void* ctx) override;
  bool SqlQueryWithoutHandler(const char* query, int flags = 0) override;
  void SqlFreeResult(void) override;
  SQL_ROW SqlFetchRow(void) override;
  const char* sql_strerror(void) override;
  void SqlDataSeek(int row) override;
  int SqlAffectedRows(void) override;
  uint64_t SqlInsertAutokeyRecord(const char* query,
                                  const char* table_name) override;
  SQL_FIELD* SqlFetchField(void) override;
  bool SqlFieldIsNotNull(int field_type) override;
  bool SqlFieldIsNumeric(int field_type) override;
  bool SqlBatchStartFileTable(JobControlRecord* jcr) override;
  bool SqlBatchEndFileTable(JobControlRecord* jcr, const char* error) override;
  bool SqlBatchInsertFileTable(JobControlRecord* jcr,
                               AttributesDbRecord* ar) override;
  bool SqlCopyStart(const std::string& table_name,
                    const std::vector<std::string>& column_names) override;
  bool SqlCopyInsert(const std::vector<DatabaseField>& data_fields) override;
  bool SqlCopyEnd() override;

 public:
  BareosDbSqlite(JobControlRecord* jcr,
                 const char* db_driver,
                 const char* db_name,
                 const char* db_user,
                 const char* db_password,
                 const char* db_address,
                 int db_port,
                 const char* db_socket,
                 bool mult_db_connections,
                 bool disable_batch_insert,
                 bool try_reconnect,
                 bool exit_on_fatal,
                 bool need_private);
  ~BareosDbSqlite();

  // Used internaly by sqlite.c to access fields in SqlQueryWithHandler()
  void SetColumnNames(char** res, int nb)
  {
    col_names_ = res;
    num_fields_ = nb;
    field_number_ = 0;
  }
};

#endif  // BAREOS_CATS_BDB_SQLITE_H_

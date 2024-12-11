import typing

def split_sql(query: str) -> typing.List[str]:
    ret = []
    c = None # current char
    p = None # previous char
    b = 0 # begin of current sql
    state = 1 # current state
    NORMAL = 1
    IDENTIFIER = 2
    SINGLE_QUOTATION = 3
    DOUBLE_QUOTATION = 4
    SINGLE_LINE_COMMENT = 5
    MULTI_LINE_COMMENT = 6
    for i in range(0, len(query)):
        c = query[i]
        if state == NORMAL:
            if c == ';':
                if i - b > 0:
                    ret.append(query[b:i])
                b = i + 1
                p = None
            elif p == '-' and c == '-':
                state = SINGLE_LINE_COMMENT
                p = None
            elif p == '/' and c == '*':
                state = MULTI_LINE_COMMENT
                p = None
            elif c == '`':
                state = IDENTIFIER
                p = None
            elif c == "'":
                state = SINGLE_QUOTATION
                p = None
            elif c == '"':
                state = DOUBLE_QUOTATION
                p = None
            else:
                p = c
        elif state == IDENTIFIER:
            if c == '`' and p != '\\':
                state = NORMAL
                p = None
            else:
                p = c
        elif state == SINGLE_QUOTATION:
            if c == "'" and p != '\\':
                state = NORMAL
                p = None
            elif p == '\\':
                p = None
            else:
                p = c
        elif state == DOUBLE_QUOTATION:
            if c == '"' and p != '\\':
                state = NORMAL
                p = None
            elif p == '\\':
                p = None
            else:
                p = c
        elif state == SINGLE_LINE_COMMENT:
            if c == '\n':
                state = NORMAL
                p = None
            else:
                p = c
        elif state == MULTI_LINE_COMMENT:
            if p == '*' and c == '/':
                state = NORMAL
                p = None
            else:
                p = c

    if b < len(query):
        ret.append(query[b:])
    return ret

# def myassert(sql, num, sqls):
#     if len(sqls) == num:
#         print('-- OK --')
#     else:
#         print('-- FAIL --')
#     print(sql)
#     for s in sqls:
#         print(f'[{s}]')

# if __name__ == "__main__":
#     sql = "select 1";
#     sqls = split_sql(sql);
#     myassert(sql, 1, sqls);

#     sql = "select 1;";
#     sqls = split_sql(sql);
#     myassert(sql, 1, sqls);

#     sql = "select 1;select 2";
#     sqls = split_sql(sql);
#     myassert(sql, 2, sqls);

#     sql = "select 1;select 2;";
#     sqls = split_sql(sql);
#     myassert(sql, 2, sqls);

#     sql = "select 1\n\n\nfrom table;";
#     sqls = split_sql(sql);
#     myassert(sql, 1, sqls);

#     sql = ";";
#     sqls = split_sql(sql);
#     myassert(sql, 0, sqls);

#     sql = ";;";
#     sqls = split_sql(sql);
#     myassert(sql, 0, sqls);

#     sql = "; ;";
#     sqls = split_sql(sql);
#     myassert(sql, 1, sqls);

#     sql = ";\n;";
#     sqls = split_sql(sql);
#     myassert(sql, 1, sqls);

#     sql = "";
#     sqls = split_sql(sql);
#     myassert(sql, 0, sqls);

#     sql = "\n";
#     sqls = split_sql(sql);
#     myassert(sql, 1, sqls);

#     sql = "select *\n-- -- ;\nfrom world\n";
#     sqls = split_sql(sql);
#     myassert(sql, 1, sqls);

#     sql = "select *\n-- -- ;\nfrom world\n";
#     sqls = split_sql(sql);
#     myassert(sql, 1, sqls);

#     sql = "select `aaaa";
#     sqls = split_sql(sql);
#     myassert(sql, 1, sqls);

#     sql = "select 'aaa;\nbbb'\n";
#     sqls = split_sql(sql);
#     myassert(sql, 1, sqls);

#     sql = "select \"--\\\"/*;\n*/\"";
#     sqls = split_sql(sql);
#     myassert(sql, 1, sqls);

#     sql = "-- line 1\nselect\n/* comment -- -- ;\n****/*\nfrom foo";
#     sqls = split_sql(sql);
#     myassert(sql, 1, sqls);

#     sql = "/*/--/*/;\nselect /* -- 1; */\n1;-- sql 2";
#     sqls = split_sql(sql);
#     myassert(sql, 3, sqls);

#     sql = """select "1\\\\";select2
# """
#     sqls = split_sql(sql);
#     myassert(sql, 2, sqls);

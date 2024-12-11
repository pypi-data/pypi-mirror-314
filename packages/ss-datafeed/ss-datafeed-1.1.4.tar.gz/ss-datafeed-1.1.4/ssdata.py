from ssdata_util import query,sqlone,query_biz
from ssdata_datasource import SS_DATASOURCE

class ssdata:
    '''
    数据操作SDK API
    '''
    def __init__(self, appId, appSec):
        self.appId = appId
        self.appSec = appSec
        self.maxRowNum = 20000
        self.buildSql_tableName = None
        self.buildSql_tableColumns = "*"
        self.buildSql_tableWhere = None
        self.buildSql_tableOrderBy = None
        self.buildSql_tableCurrPage = None
        self.buildSql_tablePagesize = 2000

    def dataset(self,sql,params=None,datasource=SS_DATASOURCE.DS_EFORM):
        result = query(self.appId,self.appSec,sql,params,
                                   datasource=datasource)
        return result
    def sqlone(self, sql, params=None, datasource=SS_DATASOURCE.DS_EFORM):
        '''
            查询单行记录

            Args：
                sql(str) 查询SQL语句
                params(map)： 查询参数列表
                datasource(dict)： 数据源（默认：DS_EFORM）

            Returns:
                返回一行数据的map

            Typical usage example:
                from ssdata_datasource import SS_DATASOURCE
                data = ssdata('xxx', 'xxxx')
                data3 = data.sqlone('select index_date,index_value from macro_base_index_values_0 where gjk_code=? and index_date>\'2019-01-01\' order by index_date',
                        'IN000006660',datasource=SS_DATASOURCE.DS_MACRO)
        '''
        result = sqlone(self.appId, self.appSec, sql, params,
                       datasource=datasource)
        return result

    def get(self, sql, params=None, datasource=SS_DATASOURCE.DS_EFORM):
        result = sqlone(self.appId, self.appSec, sql, params,
                       datasource=datasource)
        for k,v in result.items():
            return v
        return None

    def table(self,tableName, datasource=SS_DATASOURCE.DS_EFORM):
        self.buildSql_tableName = tableName
        return self

    def cols(self,cols):
        self.buildSql_tableColumns = cols
        return self

    def filter(self,where):
        self.buildSql_tableWhere = where
        return self

    def p(self,p):
        self.buildSql_tableCurrPage = p
        return self

    def ps(self,ps):
        if ps > self.maxRowNum:
            raise Exception('每页条数不能超过20000条!!!!')
        self.buildSql_tablePagesize = ps
        return self

    def orderBy(self,order):
        self.buildSql_tableOrderBy = order
        return self

    def find(self, datasource=SS_DATASOURCE.DS_EFORM):
        return self.query(datasource=datasource)

    def query(self, datasource=SS_DATASOURCE.DS_EFORM):
        if self.buildSql_tableName is None:
            raise Exception('ERROR:query操作必须指定表名!!!!')

        _sql = 'select %s from %s ' % (self.buildSql_tableColumns,self.buildSql_tableName)
        if self.buildSql_tableWhere:
            _sql = _sql + ' where 1=1 AND (%s)' % self.buildSql_tableWhere
        if self.buildSql_tableOrderBy:
            _sql = _sql + ' order by %s' % self.buildSql_tableOrderBy
        if self.buildSql_tableCurrPage:
            _sql = _sql + ' limit %d,%d' % ((self.buildSql_tableCurrPage-1)*self.buildSql_tablePagesize,self.buildSql_tablePagesize)
        else:
            _sql = _sql + ' limit %d' % self.maxRowNum
        result = query(self.appId, self.appSec, _sql, datasource=datasource)
        return result

    def page(self,sql,params=None, currPage = 1,ps=2000,datasource=SS_DATASOURCE.DS_EFORM):
        countsql = 'select count(*) num from (' + sql + ') ga'
        totalObj = sqlone(self.appId, self.appSec, countsql, params, datasource)
        num = totalObj['num']
        if num % ps == 0:
            totalPageSize = int(num / ps)
        else:
            totalPageSize = int(num / ps) + 1
        sql = 'select * from ( '+ sql + ") ga limit %d,%d" % ((currPage-1)*ps,ps)
        result = query(self.appId, self.appSec, sql, params,
                       datasource=datasource)
        return {
            'total_page':totalPageSize,
            'total_record': num,
            'result':result
        }

    # 绕过防火墙的特殊api接口
    def biz(self, bizName, params=None, currPage=1, ps=2000, datasource=SS_DATASOURCE.DS_EFORM):
        sql = None
        if bizName == 'mjsms':
            result = query_biz(self.appId, self.appSec, bizName, params = {
              'date': params.get('date'),
              'start': params.get('start',1)
            },datasource=datasource)
            return {
                'res':True,
                'result': result
            }
        return {'res':False,'msg': '没有可用的bizname，请联系管理员'}


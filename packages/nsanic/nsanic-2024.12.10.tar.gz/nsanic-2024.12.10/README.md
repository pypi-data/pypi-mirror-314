# 基于Sanic Server
  
## 设计与依赖说明  
1. 服务体系 -- 基于sanic 22.3.x 以上版本的http/websocket服务框架  
2. python环境 -- 基于3.9的async/await原生异步模型  
3. ORM -- 采用tortoise-orm -- 0.19.1 以上的异步ORM数据模型  
4. 数据库连接驱动 -- MySQL/mariaDB采用asyncmy, postgresql采用asyncpg  
5. 数据迁移工具 -- 使用aerich作为基本的数据迁移工具  
6. 缓存 -- 采用redis作为公有化基础缓存，版本建议 6.x以上  
7. 缓存驱动 -- 官方redis驱动支持，采用连接池模式  
  
## 项目说明  
参照项目目录
logs        -- 运行日志存放目录，按服务区分，服务停止情况下，删除后会自动生成  
migrations      -- 数据迁移目录，该目录下的数据一般情况不要删除或手动修改，否则会造成数据模型迁移的问题
pyproject.toml  -- 当前操作数据的服务  
非指定的其余目录皆为实际服务目录，以xi_test目录为例：  
    -- config               -- 该服务的配置存放位置  
    -- handler              -- 常规逻辑或功能处理函数或基类  
    -- model_db             -- 该服务的数据模型存放位置  
    -- model_rc             -- 该服务的缓存模型存放位置，采用内置的可直接继承自RCModel  
    -- interface            -- 该服务的接口逻辑存放位置  
    -- script               -- 该服务的定时脚本、配置脚本、自定义脚本等的存放位置    
    -- base_api.py          -- 该服务的基础接口授权相关内容  
    -- url_main.py        -- 该服务的接口路由入口  
-- http_xi_test.py/srv_xi_test.py/ws_xi_test.py   -- 服务的启动文件  
在项目根目录下 http_XXX.py/srv_XXX.py/ws_XXX.py   -- 可运行服务  以http_加服务名  


## 添加新的可启动的服务  
比如 参照示例，开启一个新的服务 xi_test，切换到相应的python环境，然后运行sanicGuider命令，按照指引生成项目，除项目名必须指定外其余均可默认  

## 关于数据迁移  
数据迁移工具采用与tortoise-orm配套的aerich迁移工具  
1. 在项目model_db下对应的服务目录下定义好数据模型, 以及对应的模型文件
2. 将需要迁移的数据模型所在的文件名添加到配置下的 MODEL_LIST内（默认是main）  不需要迁移的数据模型文件名放到MODEL_EXTRA下（默认是extra）  
MODEL_LIST = ['main', 'records']  
3. 进入项目根目录，执行 aerich init -t 服务包目录名.config.migrate_db(对应在__init__.py中的名称)  初始化数据库连接  更换服务数据库需要从该步骤重新开始执行，在同一数据库服务下，更新或回退，只参照4、5、6步骤  
4. 再执行  aerich init-db  初始化数据库  (首次迁移需要执行这一步，非首次迁移不需要这一步)
5. aerich migrate  生成迁移数据  
6. aerich upgrade  发起迁移  
7. 如有需求需要回退上一个版本执行  aerich downgrade  
  
## 关于服务部署  
这里采用service的方式启停服务，也可以采用sanic官方提供的部署方式或者直接使用supervisor运行
>采用root账户运行：   
1. 服务名称是定义的文件名，具体指定的运行账户和虚拟环境路径和启动文件路径需要在文件里进行替换  
2. 然后将配置好的服务文件移到 /etc/systemd/system/ 目录下  
3. 执行service 服务名 status/start/stop/restart  操作项目的启停和状态查看  
>采用一般账户运行(该一般账户必须被允许常驻服务)：  
1. 将服务配置】目录下配置文件内的账户指定注释掉，然后替换虚拟环境路径和启动文件路径  
2. 在用户目录的.config(隐藏目录, 没有则需要手动创建)下创建systemd/user/目录层级  
3. 将修改好的服务配置文件拷贝到账户目录：~/.config/systemd/user/ 目录下  
4. 采用 systemctl --user status/start/stop/restart 服务名 操作服务

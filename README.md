# MCP Server
## 构建步骤
### 1. 执行下面命令安装依赖包
- 创建环境
```
python -m venv mcp_server_env
```
- 激活环境
```
.\mcp_server_env\scripts\activate
```
- 安装依赖
```
pip install -r requirements.txt
```
### 2. 使用下面代码导入fastmcp
```
from fastmcp import FastMCP
```
### 3. 声名FastMCP对象, 参数为自定义MCP名字
```
mcp = FastMCP('mcp_service')
```
### 4. 添加逻辑代码
```
@mcp.tool(name='add', description="Add two numbers and return the result")
def add(a, b):
    """Add two numbers and return the result"""
    return a + b
```
#### 说明

- @mcp为第三步fastmcp的对象
- @mcp.tool 声名这个函数定义为tool
- name和description为tool的属性, 如果不写则为默认函数名称和注释

### 5. 添加运行逻辑
```
if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000, path="/mcp")
```
### 6.启动server
```
python server.py
```

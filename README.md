# pairwise-webauthn

Passkey 登录一上生产，认证器返回的响应就开始被误判：challenge 只检查长度，没有和会话里的原始 challenge 比对；origin 用 Referer 兜底，子域钓鱼页也能过；rpIdHash 没有按注册时的 RP ID 校验；UV 标志被忽略，设置里要求用户验证却接受了只存在验证；signCount 回退没有触发克隆告警；credential ID 没有按租户隔离。auth/webauthn.py 是核心，tests/test_webauthn.py 15个红。要修的是：challenge 绑定；origin/rpIdHash 严格；UV 策略；signCount 单调；credential 隔离。

## 运行

```bash
python -m pytest tests -q
```

初始状态：15 个用例失败。修复实现使全部用例通过，不要修改 `tests/` 下的测试。

子方向：其他；任务类型：Bugfix；语言/框架：Python 3, pytest；环境可复现等级：无外部依赖。

# 研究类型档案

R2 的协议骨架和 R3 的执行纪律对所有研究通用；每种研究类型真正不同的只有：对象和数据怎么选、怎样算成立、重复或稳健性怎么要求、结果中性检查长什么样、冻结什么算指纹、RESULT 要多记什么。这些差别一类一个文件放在这里，协议开头用 `- 研究类型：<文件名去掉 .md>` 声明；一篇论文用到两种时写主次，都要满足。

类型在 R1 写 FRAMING 时按下表选定，写进 `paper/FRAMING.md` 开头的 `- 研究类型：`，两种时主在前、次在后；R2 的试点与协议继承它，改类型要写理由并修订 FRAMING。

| 档案 | 适用 | 对应的 ACM SIGSOFT 经验标准 |
|---|---|---|
| [quantitative-experiment](quantitative-experiment.md) | 受控实验、基准评测、机器学习与算法比较、性能测试、仿真与优化研究 | Benchmarking、Data Science、Optimization Studies、Quantitative Simulation |
| [measurement-study](measurement-study.md) | 测量研究、实证规律、仓库挖掘、大规模观测、二手数据分析 | Repository Mining、Sampling 补充 |
| [tool-or-system-evaluation](tool-or-system-evaluation.md) | 提出工具、系统、方法并评估它 | Engineering Research、Benchmarking |
| [case-study-or-qualitative](case-study-or-qualitative.md) | 案例研究、访谈、问卷、扎根理论 | Case Study、Qualitative Surveys、Questionnaire Surveys、Grounded Theory |
| [human-subjects-experiment](human-subjects-experiment.md) | 以人为参与者的受控实验、用户研究 | Experiments (with Human Participants) |
| [formal-or-theoretical](formal-or-theoretical.md) | 形式化、理论、算法分析、机械化证明 | General Standard，无专门标准 |
| [replication](replication.md) | 复现与再现已有研究 | Replication |

评审时 `paper-review` 按同一套类型名审 L2 的十门，问法在 `paper-review/references/l2-by-method.md`。每份档案都按同一个结构写：适用；协议追加字段；判定规则与稳健性怎么写；结果中性检查长什么样；冻结什么算指纹；RESULT 追加小节；不允许的升格与常见错误；评审时对应的审法。没有合适档案的研究类型，照这个结构新写一份，文件名用小写短横线，并在本表加一行；不要把一种类型的要求硬套到另一种上。

## 来源

档案里的属性清单改写自 ACM SIGSOFT Empirical Standards（CC0，<https://github.com/acmsigsoft/EmpiricalStandards>），各档案写明对应的标准。通用骨架吸收了三处公开 skill 的做法，只取思路不取文字：K-Dense `hypothesis-generation` 与 `experimental-design`（先冻结观察、声明主张类型、分析单位与伪重复、在接触结果前给计划打时间戳、偏离要登记日期与理由）；brycewang `aer-preregistration`（主要结果少而明确、多重比较事先定、报告时先报预先设定的结果、偏离列表）；brycewang `p-hacking-skills` 的 narrative-laundering（稳健性表要有分母、试点不能消失、事后假设不能写成事前）。

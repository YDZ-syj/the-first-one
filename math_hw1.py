import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 定义符号变量
θ1, θ2, c1, c2, a, b = sp.symbols('θ1 θ2 c1 c2 a b', real=True, positive=True)

# 定义成本函数
L1 = a / sp.cos(θ1)
L2 = b / sp.cos(θ2)
C = c1 * L1 + c2 * L2

print("成本函数 C(θ₁, θ₂) =", C)

# 几何约束条件：a*tanθ₁ = b*tanθ₂
constraint = a * sp.tan(θ1) - b * sp.tan(θ2)

# 使用约束条件消去一个变量（例如用θ₂表示θ₁）
θ2_expr = sp.solve(constraint, θ2)[0]
print("约束关系 θ₂ =", θ2_expr)

# 将约束代入成本函数
C_constrained = C.subs(θ2, θ2_expr)
print("带约束的成本函数 C(θ₁) =", C_constrained)

# 对θ₁求导并令导数为零，寻找极值点
dC_dθ1 = sp.diff(C_constrained, θ1)
print("成本函数对θ₁的导数 =", dC_dθ1)

# 解方程 dC/dθ₁ = 0
optimal_condition = sp.simplify(dC_dθ1)
print("最优化条件 =", optimal_condition)

# 分析最优化条件
# 经过符号计算简化，得到 c₁*sinθ₁ = c₂*sinθ₂
optimal_solution = sp.Eq(c1 * sp.sin(θ1), c2 * sp.sin(θ2))
print("最优化解满足:", optimal_solution)


# 数值验证与可视化
# 设置具体参数进行数值验证
a_val, b_val = 10, 8  # 距离参数
c1_val, c2_val = 2, 1  # 成本参数


# 定义数值化的成本函数
def cost_function(θ1_val):
    # 根据约束条件计算θ2
    θ2_val = np.arctan(a_val * np.tan(θ1_val) / b_val)

    # 计算总成本
    L1_val = a_val / np.cos(θ1_val)
    L2_val = b_val / np.cos(θ2_val)
    return c1_val * L1_val + c2_val * L2_val, θ2_val


# 生成θ₁的取值范围（0到π/2之间，排除端点）
θ1_range = np.linspace(0.1, np.pi / 2 - 0.1, 100)
costs = []
θ2_values = []

for θ1_val in θ1_range:
    cost, θ2_val = cost_function(θ1_val)
    costs.append(cost)
    θ2_values.append(θ2_val)

# 找到最小成本对应的角度
min_cost_idx = np.argmin(costs)
optimal_θ1 = θ1_range[min_cost_idx]
optimal_θ2 = θ2_values[min_cost_idx]

print(f"最优解: θ₁ = {optimal_θ1:.3f} rad, θ₂ = {optimal_θ2:.3f} rad")
print(f"验证 c₁·sinθ₁ = {c1_val * np.sin(optimal_θ1):.3f}")
print(f"验证 c₂·sinθ₂ = {c2_val * np.sin(optimal_θ2):.3f}")

# 可视化成本函数
plt.figure(figsize=(12, 4))

# 成本随θ₁变化图
plt.subplot(1, 2, 1)
plt.plot(θ1_range, costs)
plt.axvline(optimal_θ1, color='red', linestyle='--', label=f'最优θ₁={optimal_θ1:.3f}')
plt.xlabel('θ₁ (弧度)')
plt.ylabel('总成本')
plt.title('总成本随θ₁变化')
plt.legend()
plt.grid(True)

# 验证最优条件
plt.subplot(1, 2, 2)
θ2_range = np.linspace(0.1, np.pi / 2 - 0.1, 100)
c1_sinθ1 = [c1_val * np.sin(θ1) for θ1 in θ1_range]
c2_sinθ2 = [c2_val * np.sin(θ2) for θ2 in θ2_range]

plt.plot(θ1_range, c1_sinθ1, label='c₁·sinθ₁')
plt.plot(θ2_range, c2_sinθ2, label='c₂·sinθ₂')
plt.axhline(c1_val * np.sin(optimal_θ1), color='red', linestyle='--',
            label=f'最优值={c1_val * np.sin(optimal_θ1):.3f}')
plt.xlabel('角度 (弧度)')
plt.ylabel('c·sinθ')
plt.title('验证最优条件 c₁·sinθ₁ = c₂·sinθ₂')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, RidgeCV
from sklearn.metrics import mean_squared_error

# 1. 加载数据集
file_path = "C:/Users/LuJiaWei/Desktop/Data.csv"
df = pd.read_csv(file_path)

# 2. 检查缺失值
missing_values = df.isnull().sum()
print("缺失值统计:\n", missing_values[missing_values > 0])

# 3. 目标变量 (MEDV) 分布可视化
plt.figure(figsize=(8, 5))
sns.histplot(df["MEDV"], bins=30, kde=True)
plt.title("Distribution of House Prices (MEDV)")
plt.xlabel("House Price (MEDV)")
plt.ylabel("Frequency")
plt.show()

# 4. 计算并可视化变量间的相关矩阵
plt.figure(figsize=(10, 8))
corr_matrix = df.corr()
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix")
plt.show()

# 5. 分离特征变量(X) 和 目标变量(y)
X = df.drop(columns=["MEDV"])  # 13个特征变量
y = df["MEDV"]  # 目标变量 (房价)

# 6. 划分训练集 (90%) 和 测试集 (10%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# 7. 训练线性回归模型
lin_reg = LinearRegression()
lin_reg.fit(X_train, y_train)

# 8. 计算 10 折交叉验证的 MSE
cv_mse = -cross_val_score(lin_reg, X_train, y_train, cv=10, scoring="neg_mean_squared_error").mean()

# 9. 在测试集上计算 MSE
y_pred_test = lin_reg.predict(X_test)
test_mse = mean_squared_error(y_test, y_pred_test)

print("线性回归:")
print(f"10 折交叉验证 MSE: {cv_mse:.2f}")
print(f"测试集 MSE: {test_mse:.2f}\n")

# 10. 使用 Ridge 回归并进行超参数选择 (alpha 取多个值)
alphas = np.logspace(-3, 3, 50)  # 生成 50 个 alpha 值，范围从 10^(-3) 到 10^3

# 11. 进行 10 折交叉验证选择最佳 alpha
ridge_reg = RidgeCV(alphas=alphas, cv=10, scoring="neg_mean_squared_error")
ridge_reg.fit(X_train, y_train)

# 12. 获取最佳 alpha 值
best_alpha = ridge_reg.alpha_

# 13. 计算 Ridge 回归的交叉验证 MSE 和测试集 MSE
ridge_cv_mse = -cross_val_score(ridge_reg, X_train, y_train, cv=10, scoring="neg_mean_squared_error").mean()
ridge_test_mse = mean_squared_error(y_test, ridge_reg.predict(X_test))

print("岭回归 (Ridge Regression):")
print(f"最佳 alpha: {best_alpha:.4f}")
print(f"10 折交叉验证 MSE: {ridge_cv_mse:.2f}")
print(f"测试集 MSE: {ridge_test_mse:.2f}")

# 14. 原始房价 vs 预测房价 (散点图)
plt.figure(figsize=(8, 6))
sns.scatterplot(x=y_test, y=y_pred_test)
plt.xlabel("Actual House Prices")
plt.ylabel("Predicted House Prices")
plt.title("Actual vs Predicted House Prices")
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r', lw=2)
plt.show()

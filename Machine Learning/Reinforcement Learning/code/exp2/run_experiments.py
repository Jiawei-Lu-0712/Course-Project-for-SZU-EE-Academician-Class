import subprocess
import os
import time
from datetime import datetime

def run_experiment(clip_coef, seed):
    print(f"\n开始实验: clip_coef = {clip_coef}, seed = {seed}")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 构建命令
    cmd = [
        "python", "exp5.2_lujiawei.py",
        "--seed", str(seed),
        "--clip-coef", str(clip_coef),
        "--exp-name", f"clip_coef_{clip_coef}",
        "--total-timesteps", "100000",
        "--num-envs", "4",
        "--num-steps", "128",
        "--learning-rate", "2.5e-4",
        "--torch-deterministic", "True",
        "--env-id", "CartPole-v1",
        "--cuda", "True",
        "--capture-video", "False",
        "--gae", "True",
        "--norm-adv", "True",
        "--clip-vloss", "True",
        "--ent-coef", "0.01",
        "--vf-coef", "0.5",
        "--max-grad-norm", "0.5"
    ]
    
    print("运行命令:", " ".join(cmd))
    
    try:
        # 运行命令
        subprocess.run(cmd, check=True)
        print(f"实验成功完成: clip_coef = {clip_coef}")
    except subprocess.CalledProcessError as e:
        print(f"实验失败: clip_coef = {clip_coef}")
        print(f"错误信息: {str(e)}")
    except Exception as e:
        print(f"发生未知错误: {str(e)}")
    
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

def main():
    # 设置不同的clip-coef值
    clip_coefs = [0.1, 0.2, 0.3, 0.4]
    
    # 设置固定的随机种子
    seed = 42
    
    print("开始运行实验...")
    print(f"将测试以下clip-coef值: {clip_coefs}")
    print(f"使用随机种子: {seed}")
    
    # 为每个clip-coef值运行实验
    for clip_coef in clip_coefs:
        run_experiment(clip_coef, seed)
        # 在实验之间添加短暂延迟
        time.sleep(2)
    
    print("所有实验完成！")

if __name__ == "__main__":
    main() 
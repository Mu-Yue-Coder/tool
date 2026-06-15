import streamlit as st
import numpy as np

# 设置页面标题
st.set_page_config(page_title="矩阵计算器", layout="wide")
st.title("🧮 智能矩阵计算器")
st.write("欢迎使用！请在下方选择矩阵维度并输入数值。")

# --- 侧边栏：配置参数 ---
st.sidebar.header("⚙️ 矩阵配置")
operation = st.sidebar.selectbox(
    "选择运算类型",
    ["矩阵加法 (+)", "矩阵减法 (-)", "矩阵乘法 (×)", "矩阵求逆 (⁻¹)"]
)

# 根据不同的运算，动态调整维度输入
if operation == "矩阵求逆 (⁻¹)":
    # 求逆只需要一个方阵
    n = st.sidebar.number_input("方阵维度 (N x N)", min_value=1, max_value=5, value=2)
    rows_A, cols_A = n, n
    rows_B, cols_B = 0, 0
else:
    # 其它二元运算
    st.sidebar.subheader("矩阵 A 维度")
    rows_A = st.sidebar.number_input("A 的行数", min_value=1, max_value=5, value=2)
    cols_A = st.sidebar.number_input("A 的列数", min_value=1, max_value=5, value=2)
    
    st.sidebar.subheader("矩阵 B 维度")
    if operation == "矩阵乘法 (×)":
        # 矩阵乘法要求 B 的行数等于 A 的列数
        rows_B = cols_A
        st.sidebar.text(f"B 的行数 (自动匹配 A 的列数): {rows_B}")
        cols_B = st.sidebar.number_input("B 的列数", min_value=1, max_value=5, value=2)
    else:
        # 加减法要求维度完全一致
        rows_B = rows_A
        cols_B = cols_A
        st.sidebar.text(f"B 的行数 (自动同步): {rows_B}")
        st.sidebar.text(f"B 的列数 (自动同步): {cols_B}")

# --- 主界面：矩阵输入 ---
col1, col2 = st.columns(2)

def create_matrix_input(title, rows, cols, key_prefix):
    """动态生成矩阵输入网格"""
    st.subheader(title)
    matrix = np.zeros((rows, cols))
    # 使用 st.columns 模拟网格布局
    for i in range(rows):
        cols_list = st.columns(cols)
        for j in range(cols):
            with cols_list[j]:
                matrix[i, j] = st.number_input(
                    f"[{i+1},{j+1}]", 
                    value=0.0, 
                    key=f"{key_prefix}_{i}_{j}",
                    label_visibility="collapsed" # 隐藏标签让界面更紧凑
                )
    return matrix

with col1:
    matrix_A = create_matrix_input("矩阵 A", rows_A, cols_A, "A")

with col2:
    if operation != "矩阵求逆 (⁻¹)":
        matrix_B = create_matrix_input("矩阵 B", rows_B, cols_B, "B")
    else:
        st.write("") # 占位

# --- 核心计算与结果展示 ---
st.header("📊 计算结果")

try:
    if operation == "矩阵加法 (+)":
        result = matrix_A + matrix_B
        st.write("$$A + B =$$")
        st.dataframe(result)
        
    elif operation == "矩阵减法 (-)":
        result = matrix_A - matrix_B
        st.write("$$A - B =$$")
        st.dataframe(result)
        
    elif operation == "矩阵乘法 (×)":
        result = np.dot(matrix_A, matrix_B)
        st.write("$$A \\times B =$$")
        st.dataframe(result)
        
    elif operation == "矩阵求逆 (⁻¹)":
        # 行列式不为 0 才能求逆
        det = np.linalg.det(matrix_A)
        if np.isclose(det, 0):
            st.error("❌ 矩阵的行列式为 0，不可逆！")
        else:
            result = np.linalg.inv(matrix_A)
            st.write("$$A^{-1} =$$")
            st.dataframe(result)

except Exception as e:
    st.error(f"计算过程中发生错误: {e}")
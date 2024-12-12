import subprocess


def mount_tmp(k8s_app_base_name: str):
    cmd = ('{ s3fs --version || { echo "[mount_tmp] no s3fs..." && exit 0 ;} ;} && echo "[mount_tmp] Mounting..." && '
           f's3fs {k8s_app_base_name}-tmp /tmp -o dbglevel=info -o iam_role={k8s_app_base_name}-api ')
    return subprocess.run(cmd, capture_output=True, shell=True, check=False, text=True, encoding='utf-8')  # nosec

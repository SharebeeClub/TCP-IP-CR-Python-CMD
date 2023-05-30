import threading
from dobot_api import DobotApiDashboard, DobotApi, DobotApiMove, MyType
from time import sleep
import numpy as np
import dobot_api

# 全局变量(当前坐标)
current_actual = None

def connect_robot():
    try:
        ip = "192.168.5.1"
        dashboard_p = 29999
        move_p = 30003
        feed_p = 30004
        print("正在建立连接...")
        dashboard = DobotApiDashboard(ip, dashboard_p)
        move = DobotApiMove(ip, move_p)
        feed = DobotApi(ip, feed_p)
        print(">.<连接成功>!<")
        return dashboard, move, feed
    except Exception as e:
        print(":(连接失败:(")
        raise e
#就是把这个debug文件运行不起来，韦总想先把这个debug文件运行起来，现在已经连接上机器人了
def run_point(move: DobotApiMove, point_list: list):
    # move.MovL(point_list[0], point_list[1], point_list[2], point_list[3], point_list[4], point_list[5])
    move.JointMovJ(point_list[0], point_list[1], point_list[2], point_list[3], point_list[4], point_list[5])
    
def do_gas(dashboard: DobotApiDashboard, index: int, status: int):
    dashboard.DO(index, status)
    
def get_feed(feed: DobotApi):
    global current_actual
    hasRead = 0
    while True:
        data = bytes()
        while hasRead < 1440:
            temp = feed.socket_dobot.recv(1440 - hasRead)
            if len(temp) > 0:
                hasRead += len(temp)
                data += temp
        hasRead = 0

        a = np.frombuffer(data, dtype=MyType)
        if hex((a['test_value'][0])) == '0x123456789abcdef':

            # Refresh Properties
            current_actual = a["tool_vector_actual"][0]
            print("tool_vector_actual:", current_actual)

        sleep(0.001)

def wait_arrive(point_list):
    global current_actual
    while True:
        is_arrive = True

        if current_actual is not None:
            for index in range(len(current_actual)):
                if (abs(current_actual[index] - point_list[index]) > 1):
                    is_arrive = False

            if is_arrive:
                return

        sleep(0.001)

if __name__ == '__main__':
    dashboard, move, feed = connect_robot()
    print("开始上电...")
    dashboard.PowerOn()
    print("请耐心等待,机器人正在努力启动中...")
    count = 10
    while count > 0 :
        print(count)
        count = count - 1
        sleep(1)
    print("开始使能...")
    dashboard.EnableRobot()
    print("完成使能:)")
    feed_thread = threading.Thread(target=get_feed, args=(feed,))
    feed_thread.setDaemon(True)
    feed_thread.start()
    print("循环执行...")
    
    # Joint coordinates [x,y,z,rx,ry,rz]
    # point_1 = [-176.92, -498.00, 33.44, -178.74, 1.79, -90.69]
    # point_2 = [170.53, -432.66, 221.91, -89.28, 30.71, -94.31]
    # point_3 = [169.80, -271.54, 65, 176.16, 0.09, -113.83]
    # point_4 = [170.96, -432.74, 222.14, -89.17, -42.26, -95.17]
    # point_5 = [170.21, -433.72, 223.03, -86.12, -80.95, -98.80]
    # point_6 = [170.63, -432.78, 222.12, 89.34, -21.50, 85.31]
    # point_7 = [-177.36, -498.42, 64.47, -179.73, 0.20, -90.66]
    

    point7=[57.3,69.8,79.3,-64,-90,284.5]
    point1=[57.667,74.24,77.63,-69.46,-90.76,284.505]
    point2=[86.89,62,95,-64,3.4,284]
    while True:
        run_point(move, point7)
        # wait_arrive(point7)  
        run_point(move, point1)
        # wait_arrive(point1)
        # do_gas(dashboard, 2, 1)
        # sleep(0.3)
        # do_gas(dashboard, 2, 0)
        run_point(move, point2)
        # wait_arrive(point2)
        # run_point(move, point_4)
        # wait_arrive(point_4)
        # run_point(move, point_5)
        # wait_arrive(point_5)
        # run_point(move, point_6)
        # wait_arrive(point_6)
        # run_point(move, point_3)
        # wait_arrive(point_3) 
        # do_gas(dashboard, 1, 1)
        # sleep(0.2)
        # do_gas(dashboard, 1, 0)
        
        
        

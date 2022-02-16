import constant
import math
import matplotlib.pyplot as plt

class cl_math:
    mv_debug = 0
    def switch_debug(self):
        if self.mv_debug == 0:
            self.mv_debug = 1
        else:
            self.mv_debug = 0
        return self.mv_debug
    def switch_debug9(self):
        if self.mv_debug == 0:
            self.mv_debug = 9
        else:
            self.mv_debug = 0
        return self.mv_debug
    def dprint(self, iv_output):
        if self.mv_debug > 0:
            print( iv_output )
    def dprint9(self, iv_output):
        if self.mv_debug == 9:
            print( iv_output )

    def replace_in(self, iv_equation):
        lv_result = iv_equation
        self.dprint9("replace_in 1:"+lv_result)
        lv_result=lv_result.replace("х","x")
        lv_result=lv_result.replace("²","**2")
        lv_result=lv_result.replace("³","**3")
        lv_result=lv_result.replace("√x","sqrt(x)")
        lv_result=lv_result.replace("√","sqrt")
        lv_result=lv_result.replace("pi","math.pi")

        lv_result=lv_result.replace("pow","math.pow")
        lv_result=lv_result.replace("sqrt","math.sqrt")
        lv_result=lv_result.replace("exp","math.exp")
        lv_result=lv_result.replace("expm","math.expm")
        lv_result=lv_result.replace("log","math.log")
        lv_result=lv_result.replace("log1p","math.log1p")
        lv_result=lv_result.replace("log10","math.log10")
        lv_result=lv_result.replace("log2","math.log2")

        lv_result=lv_result.replace("sin","math.sin")
        lv_result=lv_result.replace("cos","math.cos")
        lv_result=lv_result.replace("tan","math.tan")
        lv_result=lv_result.replace("tan2","math.tan2")
        lv_result=lv_result.replace("asin","math.asin")
        lv_result=lv_result.replace("acos","math.acos")
        lv_result=lv_result.replace("atan","math.atan")
        
        lv_result=lv_result.replace("degrees","math.degrees")
        lv_result=lv_result.replace("radians","math.radians")
        self.dprint9("replace_in exit:"+lv_result)
        return lv_result

    
    def normalize(self, iv_equation):
        """ Перенос левой части уравнения в правую """
        lt_fb=iv_equation.split("=")
        lv_result=lt_fb[0]
        if lt_fb[1]!='-':
            lt_fb[1]="+"+lt_fb[1]
        for lv_i in lt_fb[1]:
            if lv_i=="-":
                lv_i="+"
            else:
                if lv_i=="+":
                    lv_i='-'
            lv_result+=lv_i

        self.dprint("normalize:",lv_result)
        return self.replace_in(lv_result)

    def calculate(self, iv_equation, iv_value):
        """ Вычисление """
        lv_result = 0
        lv_equation = iv_equation.replace("x",str(iv_value))
        return (eval(lv_equation))

    def solve_universal(self, iv_equation, iv_min, iv_max, iv_accuracy):
        lv_min, lv_max = iv_min, iv_max
        if (self.calculate(iv_equation, lv_min) * self.calculate(iv_equation, lv_max) < 0):
            if self.calculate(iv_equation, lv_min) > 0:
                lv_min,lv_max=lv_max,lv_min

            while(abs(lv_min-lv_max) > iv_accuracy):
                lv_new=(lv_min+lv_max)/2
                if(self.calculate(iv_equation, lv_new)<0):
                    lv_min=lv_new
                else:
                    lv_max=lv_new
            lv_x = lv_new
        else:
            return constant.gc_error_select_other_range
        return math.ceil(lv_x*constant.gc_ceil)/constant.gc_ceil
    
    def linear_equation(self, iv_equation):
        """ Линейное уравнение """
        lv_x = 'Решаем линейное уравнение' + iv_equation
        return lv_x

    def quadratic_equation(self, iv_equation):
        """ Квадратное уравнение """
        lv_x = 'Решаем квадратное уравнение' + iv_equation
        return lv_x
    
    def main(self, iv_cmd, iv_equation, iv_min, iv_max):
        print("main", iv_equation, iv_min, iv_max)
        """ Главная функция класса """
        lv_response=""
        if iv_min == iv_max:
            return constant.gc_error_in_range
        #print("main 1", iv_equation, iv_min, iv_max)
        try:
            lv_min = float(iv_min)
        except:
            return constant.gc_error_in_num+iv_min

        try:
            lv_max = float(iv_max)
        except:
            return constant.gc_error_in_num+iv_max
        #print("main 2", iv_equation, lv_min, lv_max)
        try:
            self.calculate( lv_equation, lv_min)
            self.calculate( lv_equation, lv_max)
        except:
            lv_response = constant.gc_error_equation
        # print("main 3", iv_equation, lv_min, lv_max)

        try:
            lv_equation = self.normalize(iv_equation.lower())
            # print("main 4", lv_equation, lv_min, lv_max)
            if iv_cmd == self.gc_cmd_linear_equation:
                lv_response = self.linear_equation( iv_equation )
            elif iv_cmd == self.gc_cmd_quadratic_equation:
                lv_response = self.quadratic_equation( iv_equation )
            else:
                lv_response = self.solve_universal( lv_equation, lv_min, lv_max, constant.gc_accuracy )
        except:
            lv_response = constant.gc_error_equation
        return lv_response
        
    def tab(self, iv_equation, iv_min, iv_max):
        self.dprint("table equation:" + iv_equation + " min:"+iv_min+ " max:"+iv_max)
        lv_equation = self.replace_in(iv_equation)
        self.dprint("table equation:" + lv_equation )
        try:
            lv_min = float(iv_min)
        except:
            return constant.gc_error_in_num+iv_min

        try:
            lv_max = float(iv_max)
        except:
            return constant.gc_error_in_num+iv_max
        if lv_min > lv_max:
            lv_min, lv_max = lv_max, lv_min
        self.dprint9("table 1 equation:" + lv_equation + " min:"+str(lv_min)+ " max:"+str(lv_max))
        lv_x = lv_min
        self.dprint9("table 1.1 equation:" + lv_equation + " min:"+str(lv_min)+ " max:"+str(lv_max)+" tab_count:"+str(constant.gc_tab_count))
        lv_step = (lv_max-lv_min)/constant.gc_tab_count
        self.dprint("table equation:" + lv_equation + " x:"+str(lv_x)+ "step:"+str(lv_step))
        lv_response = ""
        while lv_x <= lv_max:
            lv_y = self.calculate(lv_equation, lv_x)
            self.dprint9("tab:"+ lv_equation + " x:"+ str(lv_x) + " y:" + str( lv_y ))
            lv_response = lv_response + str( lv_x ) + "," + str( lv_y ) + "\n"
            lv_x += lv_step
        return lv_response
        
    def graph(self, iv_equation, iv_min, iv_max):
        self.dprint("graph equation:" + iv_equation + " min:"+iv_min+ "max:"+iv_max)
        lv_equation = self.replace_in(iv_equation.lower())
        self.dprint("graph 1 equation:"+ lv_equation)
        try:
            lv_min = float(iv_min)
        except:
            return constant.gc_error_in_num+iv_min

        try:
            lv_max = float(iv_max)
        except:
            return constant.gc_error_in_num+iv_max
        if lv_min > lv_max:
            lv_min, lv_max = lv_max, lv_min
        lv_x = float(iv_min)
        lv_step = (lv_max-lv_min)/constant.gc_graph_count

        self.dprint("tab 2 equation:"+ lv_equation + " min:"+ str(lv_min) + " max:" + str(lv_max) + " step :" + str(lv_step))
        # print("graph 2", lv_step)
        while lv_x <= lv_max:
            lv_y = self.calculate(lv_equation, lv_x)
            self.dprint9("graph2 ["+ str(lv_x) + ","+ str(lv_y)+"]")
            plt.scatter(lv_x,lv_y)
            lv_x += lv_step
            self.dprint9("graph3 ["+ str(lv_x) + ","+ str(lv_y)+"]")

        plt.savefig(constant.gc_graph_file_name)
        plt.clf()
        return constant.gc_graph_file_name

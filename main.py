#from takip import create_entry, read_all_entries, update_entry, delete_entry
import json
from paramiko import sftp as ssh
import schedule
import time
import re
import rest

proje = {}

json_str = '{"@timestamp":"2023-11-13T13:35:32.446+03:00","@version":1,"message":"Aritmetik hata oldu","logger_name":"tr.gov.ptt.SosyalFaturaElektrik.controller.ElektrikHamController","thread_name":"http-nio-9908-exec-2","level":"ERROR","level_value":40000,"stack_trace":"java.lang.ArithmeticException: / by zerotat tr.gov.ptt.SosyalFaturaElektrik.controller.ElektrikHamController.hataver(ElektrikHamController.java:79)tat java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)tat java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77)tat java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)tat java.base/java.lang.reflect.Method.invoke(Method.java:568)tat org.springframework.aop.support.AopUtils.invokeJoinpointUsingReflection(AopUtils.java:343)tat org.springframework.aop.framework.ReflectiveMethodInvocation.invokeJoinpoint(ReflectiveMethodInvocation.java:196)tat org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:163)tat org.springframework.aop.framework.CglibAopProxy$CglibMethodInvocation.proceed(CglibAopProxy.java:750)tat org.springframework.aop.framework.adapter.AfterReturningAdviceInterceptor.invoke(AfterReturningAdviceInterceptor.java:57)tat org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:184)tat org.springframework.aop.framework.CglibAopProxy$CglibMethodInvocation.proceed(CglibAopProxy.java:750)tat org.springframework.aop.framework.adapter.MethodBeforeAdviceInterceptor.invoke(MethodBeforeAdviceInterceptor.java:58)tat org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:184)tat org.springframework.aop.framework.CglibAopProxy$CglibMethodInvocation.proceed(CglibAopProxy.java:750)tat org.springframework.aop.interceptor.ExposeInvocationInterceptor.invoke(ExposeInvocationInterceptor.java:97)tat org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:184)tat org.springframework.aop.framework.CglibAopProxy$CglibMethodInvocation.proceed(CglibAopProxy.java:750)tat org.springframework.aop.framework.CglibAopProxy$DynamicAdvisedInterceptor.intercept(CglibAopProxy.java:702)tat tr.gov.ptt.SosyalFaturaElektrik.controller.ElektrikHamController$$SpringCGLIB$$0.hataver(<generated>)tat java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)tat java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77)tat java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)tat java.base/java.lang.reflect.Method.invoke(Method.java:568)tat org.springframework.web.method.support.InvocableHandlerMethod.doInvoke(InvocableHandlerMethod.java:207)tat org.springframework.web.method.support.InvocableHandlerMethod.invokeForRequest(InvocableHandlerMethod.java:152)tat org.springframework.web.servlet.mvc.method.annotation.ServletInvocableHandlerMethod.invokeAndHandle(ServletInvocableHandlerMethod.java:118)tat org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.invokeHandlerMethod(RequestMappingHandlerAdapter.java:884)tat org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.handleInternal(RequestMappingHandlerAdapter.java:797)tat org.springframework.web.servlet.mvc.method.AbstractHandlerMethodAdapter.handle(AbstractHandlerMethodAdapter.java:87)tat org.springframework.web.servlet.DispatcherServlet.doDispatch(DispatcherServlet.java:1081)tat org.springframework.web.servlet.DispatcherServlet.doService(DispatcherServlet.java:974)tat org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:1011)tat org.springframework.web.servlet.FrameworkServlet.doGet(FrameworkServlet.java:903)tat jakarta.servlet.http.HttpServlet.service(HttpServlet.java:564)tat org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:885)tat jakarta.servlet.http.HttpServlet.service(HttpServlet.java:658)tat org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:205)tat org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:149)tat org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:51)tat org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:174)tat org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:149)tat org.springframework.web.filter.RequestContextFilter.doFilterInternal(RequestContextFilter.java:100)tat org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:116)tat org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:174)tat org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:149)tat org.springframework.web.filter.FormContentFilter.doFilterInternal(FormContentFilter.java:93)tat org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:116)tat org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:174)tat org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:149)tat org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(CharacterEncodingFilter.java:201)tat org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:116)tat org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:174)tat org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:149)tat org.apache.catalina.core.StandardWrapperValve.invoke(StandardWrapperValve.java:166)tat org.apache.catalina.core.StandardContextValve.invoke(StandardContextValve.java:90)tat org.apache.catalina.authenticator.AuthenticatorBase.invoke(AuthenticatorBase.java:482)tat org.apache.catalina.core.StandardHostValve.invoke(StandardHostValve.java:115)tat org.apache.catalina.valves.ErrorReportValve.invoke(ErrorReportValve.java:93)tat org.apache.catalina.core.StandardEngineValve.invoke(StandardEngineValve.java:74)tat org.apache.catalina.connector.CoyoteAdapter.service(CoyoteAdapter.java:341)tat org.apache.coyote.http11.Http11Processor.service(Http11Processor.java:390)tat org.apache.coyote.AbstractProcessorLight.process(AbstractProcessorLight.java:63)tat org.apache.coyote.AbstractProtocol$ConnectionHandler.process(AbstractProtocol.java:894)tat org.apache.tomcat.util.net.NioEndpoint$SocketProcessor.doRun(NioEndpoint.java:1741)tat org.apache.tomcat.util.net.SocketProcessorBase.run(SocketProcessorBase.java:52)tat org.apache.tomcat.util.threads.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1191)tat org.apache.tomcat.util.threads.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:659)tat org.apache.tomcat.util.threads.TaskThread$WrappingRunnable.run(TaskThread.java:61)tat java.base/java.lang.Thread.run(Thread.java:833)"}'

def read_remote_log_file():

    konum = None

    ssh_client = ssh.SSHClient()
    ssh_client.set_missing_host_key_policy(ssh.AutoAddPolicy())

    # Sunucu bilgileri
    hostname = 'uzak_sunucu_ip_adresi'
    username = 'kullanici_adi'
    password = 'sifre'

    try:
        ssh_client.connect(hostname, username=username, password=password)
        sftp = ssh_client.open_sftp()

        remote_log_path = '/uzak/dizin/logdosyasi.log'

        with sftp.file(remote_log_path, 'r') as dosya:
            dosya.seek(0 if not konum else konum)
            for satir in dosya:
                print(satir)
                konum = dosya.tell()

    except Exception as e:
        print(f"Hata: {e}")

    finally:
        sftp.close()
        ssh_client.close()

def get_regex_values(desen, metin):

    eslesmeler = re.findall(desen, metin)
    return eslesmeler


def get_json_values(json_str, variable_name):
    try:

        data = json.loads(json_str)

        value = data.get(variable_name)

        if value is not None:
            return value
        else:
            return f"{variable_name} bulunamadı."

    except json.JSONDecodeError as e:
        return f"Hata: JSON çözümlenemedi. {e}"

def is_json(string):
    try:
        json.loads(string)
        return True
    except ValueError:
        return False


def load_projects():

    return

if __name__ == "__main__":
    # create_entry('2023-11-12', 'example', 'GET', 'None')
    # update_entry(1, 'Updated error message')
    # read_all_entries()

    logger_name_value = get_json_values(json_str, 'logger_name')
    print(logger_name_value)
    rest.app.run()


# schedule.every(5).minutes.do(read_remote_log_file)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)

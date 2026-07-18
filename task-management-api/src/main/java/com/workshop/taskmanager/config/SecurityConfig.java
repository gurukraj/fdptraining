package com.workshop.taskmanager.config;

import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.io.IOException;

/**
 * Simple header-based authentication for workshop purposes.
 * In production, use Spring Security with JWT or OAuth2.
 *
 * Headers:
 * - X-User-Id: identifies the user (defaults to "anonymous")
 * - X-User-Role: "ADMIN" or "USER" (defaults to "USER")
 */
@Configuration
public class SecurityConfig {

    @Bean
    public FilterRegistrationBean<UserContextFilter> userContextFilter() {
        FilterRegistrationBean<UserContextFilter> registrationBean = new FilterRegistrationBean<>();
        registrationBean.setFilter(new UserContextFilter());
        registrationBean.addUrlPatterns("/api/*");
        registrationBean.setOrder(1);
        return registrationBean;
    }

    public static class UserContextFilter implements Filter {

        @Override
        public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
                throws IOException, ServletException {

            HttpServletRequest httpRequest = (HttpServletRequest) request;

            // Extract user info from headers with defaults
            String userId = httpRequest.getHeader("X-User-Id");
            if (userId == null || userId.isBlank()) {
                userId = "anonymous";
            }

            String userRole = httpRequest.getHeader("X-User-Role");
            if (userRole == null || userRole.isBlank()) {
                userRole = "USER";
            }

            // Store in request attributes for controllers to access
            httpRequest.setAttribute("userId", userId);
            httpRequest.setAttribute("userRole", userRole.toUpperCase());

            chain.doFilter(request, response);
        }
    }

    /**
     * Utility method to extract userId from request attributes.
     */
    public static String getUserId(HttpServletRequest request) {
        Object userId = request.getAttribute("userId");
        return userId != null ? userId.toString() : "anonymous";
    }

    /**
     * Utility method to check if the current user is an admin.
     */
    public static boolean isAdmin(HttpServletRequest request) {
        Object role = request.getAttribute("userRole");
        return "ADMIN".equals(role != null ? role.toString() : "USER");
    }
}

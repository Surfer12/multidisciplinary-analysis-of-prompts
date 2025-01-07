# Docker Environment Walkthrough

This guide provides step-by-step instructions for launching and using the Computer Use Demo with meta-cognitive tools in Docker.

## Initial Setup

1. **Environment Setup**
```bash
# Clone the repository
git clone https://github.com/yourusername/analysis-of-prompts.git
cd analysis-of-prompts

# Create environment file
cat > .env << EOL
ANTHROPIC_API_KEY=your_api_key_here
CLOUD_ML_REGION=your_region  # Optional, for Google Cloud
EOL

# Create log directory
mkdir -p logs
```

2. **Build and Launch**
```bash
# Build and start the container
docker-compose up --build

# In a separate terminal, verify the container is running
docker-compose ps
```

## Accessing the Interface

1. **Web Interface**: Open http://localhost:8501 in your browser
2. **VNC Access** (for debugging): Connect to localhost:5900 using a VNC viewer

## Using Meta-Cognitive Tools

### 1. Pattern Recognition

The demo now includes pattern recognition capabilities. Here's how to use them:

```python
# Example interaction in the chat interface
"Take a screenshot of the current window"
# The tool will:
# - Track state changes
# - Analyze execution patterns
# - Monitor resource usage
# - Display insights in the sidebar
```

### 2. Adaptive Behavior

The system adapts based on resource usage and performance:

1. **Resource-Intensive Operations**
   ```python
   # Example: Large screenshot
   "Take a screenshot of the entire screen at high resolution"
   # The system will:
   # - Monitor resource usage
   # - Adapt parameters if needed
   # - Show adaptation reasons in the UI
   ```

2. **Repeated Operations**
   ```python
   # Example: Multiple clicks
   "Click at coordinates (100,100) five times"
   # The system will:
   # - Detect patterns
   # - Optimize execution
   # - Show performance metrics
   ```

### 3. Performance Monitoring

Monitor tool performance in real-time:

1. **Metrics Dashboard**
   - View execution stability
   - Track pattern diversity
   - Monitor resource usage
   - See adaptation history

2. **Tool History**
   - Access execution logs
   - View pattern analysis
   - Track adaptations
   - Monitor performance trends

## Advanced Features

### 1. Custom Pattern Analysis

```python
# Configure pattern sensitivity
"Configure pattern analysis with sensitivity 0.8"
# The system will adjust pattern detection thresholds
```

### 2. Adaptation Control

```python
# Set adaptation thresholds
"Set resource adaptation threshold to 70%"
# The system will adjust when to trigger adaptations
```

### 3. Performance Tuning

```python
# Monitor specific metrics
"Enable detailed performance monitoring for screenshot operations"
# The system will provide enhanced metrics for screenshots
```

## Debugging and Monitoring

### 1. Access Container Logs
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f computer-use-demo
```

### 2. VNC Debugging
```bash
# Connect to VNC for visual debugging
vncviewer localhost:5900
```

### 3. Container Shell Access
```bash
# Access container shell
docker-compose exec computer-use-demo bash

# Check system status
top
htop  # if installed
```

## Common Workflows

### 1. Basic Interaction with Pattern Recognition
```python
# 1. Take screenshot
"Take a screenshot of the browser window"

# 2. View patterns
Check the "Execution Patterns" section in sidebar

# 3. Monitor adaptations
Check the "Tool Adaptations" section for any adjustments
```

### 2. Resource-Intensive Operations
```python
# 1. Start resource-heavy task
"Process and analyze multiple screenshots"

# 2. Monitor performance
Watch the Performance Metrics dashboard

# 3. Review adaptations
Check adaptation logs for automatic adjustments
```

### 3. Pattern Learning
```python
# 1. Perform repeated actions
"Click through a sequence of coordinates"

# 2. View learned patterns
Check Pattern Analysis in the insights tab

# 3. Apply optimizations
The system will automatically optimize similar sequences
```

## Troubleshooting

### 1. Connection Issues
```bash
# Check container status
docker-compose ps

# Restart container
docker-compose restart

# Check logs for errors
docker-compose logs -f
```

### 2. Performance Issues
```bash
# Monitor resource usage
docker stats

# Check container limits
docker-compose exec computer-use-demo top

# Adjust resource limits in docker-compose.yml if needed
```

### 3. Display Problems
```bash
# Restart X server
docker-compose exec computer-use-demo ./start_xvfb.sh

# Check X server logs
docker-compose exec computer-use-demo cat /var/log/Xvfb.1.log
```

## Best Practices

1. **Regular Monitoring**
   - Check performance metrics regularly
   - Review adaptation logs
   - Monitor resource usage

2. **Pattern Analysis**
   - Allow system to learn from repeated operations
   - Review pattern insights
   - Adjust sensitivity as needed

3. **Resource Management**
   - Monitor container resources
   - Adjust limits if needed
   - Review adaptation thresholds

4. **Debugging**
   - Use VNC for visual verification
   - Check logs for issues
   - Monitor system metrics

## Next Steps

1. **Customize Configurations**
   - Adjust pattern recognition sensitivity
   - Modify adaptation thresholds
   - Configure monitoring intervals

2. **Extend Functionality**
   - Add custom pattern types
   - Implement new observers
   - Create custom visualizations

3. **Integration**
   - Connect with external monitoring
   - Add custom metrics
   - Implement additional adaptations
